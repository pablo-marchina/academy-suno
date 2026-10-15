"""Map native editorial format units into the bounded M05 financial consistency gate.

The native format contracts carry SourceRef.claim_id and ProvenanceRef; they do
NOT carry a parsed numeric assertion. An independent supplied FinancialAssertion
is always required. This bridge never parses prose or certifies original PDFs.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

from suno_content.consistency.engine import (
    ConsistencyBundle,
    FinancialAssertion,
    FinancialFact,
    VariantAssertions,
    evaluate_consistency,
)
from suno_content.domain import (
    AudienceLevel,
    GateStatus,
    OutputFormat,
    SourceProvenance,
    VariantSpec,
)
from suno_content.formats import (
    ArticleOutput,
    CarouselOutput,
    FormatOutput,
    ShortVideoOutput,
    SourceRef,
)

VERSION = "native_claim_bridge.v1"


class NativeEvidenceError(ValueError):
    """Invalid identity, disconnected source or ambiguous authoring handoff."""


@dataclass(frozen=True, slots=True)
class NativeVariant:
    """Paired native output + supplied factual assertion catalog for one job."""

    spec: VariantSpec
    output: FormatOutput
    assertions: tuple[FinancialAssertion, ...]
    upstream_gates: Mapping[str, GateStatus]


@dataclass(frozen=True, slots=True)
class NativeUnit:
    """A complete native block, not a claim inferred from raw text."""

    path: str
    text: str
    refs: tuple[SourceRef, ...]


def _units(output: FormatOutput) -> tuple[NativeUnit, ...]:
    if isinstance(output, ArticleOutput):
        return tuple(
            NativeUnit(
                path=f"sections[{section_index}].paragraphs[{paragraph_index}]",
                text=paragraph.text,
                refs=paragraph.source_refs,
            )
            for section_index, section in enumerate(output.sections)
            for paragraph_index, paragraph in enumerate(section.paragraphs)
        )
    if isinstance(output, CarouselOutput):
        return tuple(
            NativeUnit(
                path=f"slides[{slide.slide_index}]",
                text=f"{slide.headline}\n{slide.body}",
                refs=slide.source_refs,
            )
            for slide in output.slides
        )
    if isinstance(output, ShortVideoOutput):
        return tuple(
            NativeUnit(
                path=f"segments[{index}]",
                text=(
                    f"{segment.narration}\n{segment.on_screen_text}"
                    if segment.on_screen_text is not None else segment.narration
                ),
                refs=segment.source_refs,
            )
            for index, segment in enumerate(output.segments)
        )
    raise NativeEvidenceError("unsupported native output type")


def _lineage_guard(ref: SourceRef, source: SourceProvenance) -> None:
    if ref.source_id != source.source_id or ref.source_hash != source.source_hash:
        raise NativeEvidenceError("native source reference lineage mismatch")


def _ref_ids(refs: Iterable[SourceRef]) -> frozenset[str]:
    return frozenset(ref.provenance.canonical_json() for ref in refs)


def _combine(*states: GateStatus) -> GateStatus:
    if GateStatus.FAIL in states:
        return GateStatus.FAIL
    if GateStatus.REVIEW_REQUIRED in states:
        return GateStatus.REVIEW_REQUIRED
    return GateStatus.PASS


def evaluate_native_outputs(
    *,
    run_id: str,
    source: SourceProvenance,
    source_ledger_version: str,
    facts: tuple[FinancialFact, ...],
    outputs: tuple[NativeVariant, ...],
) -> dict[str, object]:
    """Audit native claim bindings then run W010-T001 structured consistency.

    A reported PASS only establishes internal consistency of the *provided*
    native refs, supplied assertions, source fact catalog and upstream gates.
    It is not text semantic coverage, financial correctness or production proof.
    """
    if not isinstance(source, SourceProvenance):
        raise NativeEvidenceError("source must be canonical SourceProvenance")
    known_fact_ids = {fact.fact_id for fact in facts}
    if len(known_fact_ids) != len(facts):
        raise NativeEvidenceError("duplicate source fact ID")
    issues: list[dict[str, str]] = []
    variants: list[VariantAssertions] = []
    job_ids: set[str] = set()
    pairs: set[tuple[AudienceLevel, OutputFormat]] = set()

    for item in outputs:
        spec = item.spec
        if not isinstance(spec, VariantSpec):
            raise NativeEvidenceError("every native variant requires a canonical VariantSpec")
        if not isinstance(item.output, (ArticleOutput, CarouselOutput, ShortVideoOutput)):
            raise NativeEvidenceError("native output type invalid")
        if spec.source != source:
            raise NativeEvidenceError("variant source identity/hash mismatches run source")
        if spec.format != item.output.format:
            raise NativeEvidenceError("native output format differs from VariantSpec")
        if spec.job_id in job_ids:
            raise NativeEvidenceError("duplicate native job_id")
        pair = (spec.audience, spec.format)
        if pair in pairs:
            raise NativeEvidenceError("duplicate native audience/format branch")
        job_ids.add(spec.job_id)
        pairs.add(pair)

        units = _units(item.output)
        bound: dict[str, list[tuple[NativeUnit, SourceRef]]] = {}
        for unit in units:
            for ref in unit.refs:
                _lineage_guard(ref, source)
                if ref.claim_id is not None:
                    if ref.claim_id not in known_fact_ids:
                        raise NativeEvidenceError("native claim ref missing source fact")
                    bound.setdefault(ref.claim_id, []).append((unit, ref))

        if isinstance(item.output, ArticleOutput):
            for ref in item.output.source_refs:
                _lineage_guard(ref, source)
                if ref.claim_id is not None and ref.claim_id not in bound:
                    issues.append({
                        "code": "ARTICLE_METADATA_ONLY_CLAIM",
                        "decision": "REVIEW_REQUIRED",
                        "job_id": spec.job_id,
                        "claim_id": ref.claim_id,
                        "path": "source_refs",
                    })

        asserted_ids = {a.fact_id for a in item.assertions}
        if len(asserted_ids) != len(item.assertions):
            raise NativeEvidenceError("duplicate typed assertion fact_id")
        if asserted_ids - known_fact_ids:
            raise NativeEvidenceError("typed assertion missing source fact")
        for claim_id, occurrences in sorted(bound.items()):
            if claim_id not in asserted_ids:
                issues.append({
                    "code": "NATIVE_ANCHOR_WITHOUT_TYPED_ASSERTION",
                    "decision": "REVIEW_REQUIRED",
                    "job_id": spec.job_id,
                    "claim_id": claim_id,
                    "path": ",".join(sorted({u.path for u, _ in occurrences})),
                })
        for assertion in item.assertions:
            occurrences = bound.get(assertion.fact_id, [])
            if not occurrences:
                issues.append({
                    "code": "TYPED_ASSERTION_NOT_ANCHORED_IN_NATIVE_UNIT",
                    "decision": "REVIEW_REQUIRED",
                    "job_id": spec.job_id,
                    "claim_id": assertion.fact_id,
                    "path": "none",
                })
                continue
            unique_units = {u.path for u, _ in occurrences}
            if len(unique_units) != 1:
                issues.append({
                    "code": "MULTIPLE_NATIVE_UNITS_REQUIRE_PER_UNIT_REVIEW",
                    "decision": "REVIEW_REQUIRED",
                    "job_id": spec.job_id,
                    "claim_id": assertion.fact_id,
                    "path": ",".join(sorted(unique_units)),
                })
            if _ref_ids(ref for _, ref in occurrences) != frozenset(
                p.canonical_json() for p in assertion.provenance
            ):
                issues.append({
                    "code": "NATIVE_TYPED_ASSERTION_PROVENANCE_MISMATCH",
                    "decision": "REVIEW_REQUIRED",
                    "job_id": spec.job_id,
                    "claim_id": assertion.fact_id,
                    "path": ",".join(sorted(unique_units)),
                })
            if assertion.rendered_text not in {u.text for u, _ in occurrences}:
                issues.append({
                    "code": "TYPED_ASSERTION_TEXT_NOT_BOUND_TO_NATIVE_UNIT",
                    "decision": "REVIEW_REQUIRED",
                    "job_id": spec.job_id,
                    "claim_id": assertion.fact_id,
                    "path": ",".join(sorted(unique_units)),
                })
        variants.append(
            VariantAssertions(
                job_id=spec.job_id,
                audience=spec.audience,
                output_format=spec.format,
                upstream_gates=dict(item.upstream_gates),
                assertions=item.assertions,
            )
        )
    bundle = ConsistencyBundle(
        run_id=run_id,
        source=source,
        source_ledger_version=source_ledger_version,
        facts=facts,
        variants=tuple(variants),
    )
    structured = evaluate_consistency(bundle)
    bridge_status = GateStatus.REVIEW_REQUIRED if issues else GateStatus.PASS
    status = _combine(GateStatus(structured["status"]), bridge_status)
    return {
        "schema_version": "native_claim_bridge_report.v1",
        "bridge_version": VERSION,
        "run_id": run_id,
        "status": status.value,
        "native_binding_status": bridge_status.value,
        "native_binding_findings": issues,
        "structured_consistency": structured,
        "observed_native_formats": sorted({item.spec.format.value for item in outputs}),
        "native_job_count": len(job_ids),
        "human_gold_eligible": False,
        "text_semantic_claim_extraction_observed": False,
        "source_original_verified_by_bridge": False,
        "nine_provider_outputs_observed": False,
        "production_ready": False,
    }
