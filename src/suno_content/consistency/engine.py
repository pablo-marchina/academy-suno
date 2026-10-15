"""Bounded M05 deterministic structured-claim consistency across canonical 3x3 variants.

All input assertions are supplied by a caller; this code does not extract
claims from prose or validate an original PDF. Never use it as a production
quality/reader-comprehension claim on synthetic fixtures.
"""
from __future__ import annotations

from collections import defaultdict
from decimal import Decimal, InvalidOperation
from typing import Annotated, Literal

from pydantic import Field, StringConstraints, field_validator, model_validator

from suno_content.domain import (
    AudienceLevel,
    DomainModel,
    GateStatus,
    Materiality,
    OutputFormat,
    ProvenanceRef,
    SourceProvenance,
)

VERSION = "cross_output_consistency.v1"
NonEmpty = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
Modality = Literal["ACTUAL", "FORECAST", "CONDITIONAL"]
Direction = Literal["UP", "DOWN", "UNCHANGED", "NOT_APPLICABLE"]
REQUIRED_GATES = frozenset({"source", "factual", "policy", "schema", "provenance"})
BRANCHES = frozenset(
    (audience, fmt)
    for audience in AudienceLevel
    for fmt in OutputFormat
)


def _finite_decimal(value: object) -> Decimal:
    """Exact decimal, never an inexact binary float or non-finite value."""
    if isinstance(value, bool) or isinstance(value, (float, int)):
        raise ValueError("financial values require a decimal string, not bool/float/int")
    if not isinstance(value, (str, Decimal)):
        raise ValueError("financial value must be a decimal string")
    try:
        number = Decimal(value)
    except (InvalidOperation, ValueError) as exc:
        raise ValueError("invalid financial decimal value") from exc
    if not number.is_finite():
        raise ValueError("financial value must be finite")
    return number


class FinancialFact(DomainModel):
    """A *provided* source-anchored reference fact (not independently extracted)."""

    schema_version: Literal["financial_fact.v1"] = "financial_fact.v1"
    fact_id: NonEmpty
    value: Decimal
    unit: NonEmpty
    period: NonEmpty
    modality: Modality
    condition: NonEmpty | None = None
    direction: Direction
    materiality: Materiality
    required_for_all: bool = False
    provenance: Annotated[tuple[ProvenanceRef, ...], Field(min_length=1)]
    source_gate: GateStatus

    @field_validator("value", mode="before")
    @classmethod
    def validate_value(cls, value: object) -> Decimal:
        return _finite_decimal(value)

    @model_validator(mode="after")
    def coherent_modality(self) -> "FinancialFact":
        if self.modality == "CONDITIONAL" and not self.condition:
            raise ValueError("conditional source fact requires named condition")
        if self.modality != "CONDITIONAL" and self.condition is not None:
            raise ValueError("condition is only valid for CONDITIONAL modality")
        if len({p.canonical_json() for p in self.provenance}) != len(self.provenance):
            raise ValueError("duplicate source fact provenance")
        return self


class FinancialAssertion(DomainModel):
    """Structured assertion made in a specific output about fact_id."""

    schema_version: Literal["financial_assertion.v1"] = "financial_assertion.v1"
    fact_id: NonEmpty
    value: Decimal
    unit: NonEmpty
    period: NonEmpty
    modality: Modality
    condition: NonEmpty | None = None
    direction: Direction
    provenance: Annotated[tuple[ProvenanceRef, ...], Field(min_length=1)]
    rendered_text: NonEmpty

    @field_validator("value", mode="before")
    @classmethod
    def validate_value(cls, value: object) -> Decimal:
        return _finite_decimal(value)

    @model_validator(mode="after")
    def coherent_modality(self) -> "FinancialAssertion":
        if self.modality == "CONDITIONAL" and not self.condition:
            raise ValueError("conditional assertion needs explicit condition")
        if self.modality != "CONDITIONAL" and self.condition is not None:
            raise ValueError("condition is only valid for CONDITIONAL modality")
        if len({p.canonical_json() for p in self.provenance}) != len(self.provenance):
            raise ValueError("duplicate assertion provenance")
        return self


class VariantAssertions(DomainModel):
    schema_version: Literal["variant_assertions.v1"] = "variant_assertions.v1"
    job_id: NonEmpty
    audience: AudienceLevel
    output_format: OutputFormat
    upstream_gates: dict[str, GateStatus]
    assertions: tuple[FinancialAssertion, ...] = ()

    @model_validator(mode="after")
    def unique_claims_and_gates(self) -> "VariantAssertions":
        if set(self.upstream_gates) != REQUIRED_GATES:
            raise ValueError("five canonical source/factual/policy/schema/provenance gates are required")
        ids = [a.fact_id for a in self.assertions]
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate fact_id assertions inside one variant")
        return self


class ConsistencyBundle(DomainModel):
    schema_version: Literal["cross_output_bundle.v1"] = "cross_output_bundle.v1"
    run_id: NonEmpty
    source: SourceProvenance
    source_ledger_version: NonEmpty
    facts: Annotated[tuple[FinancialFact, ...], Field(min_length=1)]
    variants: tuple[VariantAssertions, ...]

    @model_validator(mode="after")
    def validate_lineage(self) -> "ConsistencyBundle":
        facts = {fact.fact_id for fact in self.facts}
        if len(facts) != len(self.facts):
            raise ValueError("duplicate source fact_id")
        pairs = [(v.audience, v.output_format) for v in self.variants]
        if len(pairs) != len(set(pairs)):
            raise ValueError("duplicate 3x3 branch")
        jobs = [v.job_id for v in self.variants]
        if len(jobs) != len(set(jobs)):
            raise ValueError("duplicate job IDs")
        if any(pair not in BRANCHES for pair in pairs):
            raise ValueError("invalid 3x3 branch")
        lineage = (self.source.source_id, self.source.source_hash)
        for fact in self.facts:
            if any((p.source_id, p.source_hash) != lineage for p in fact.provenance):
                raise ValueError("source fact provenance points outside run source")
        for variant in self.variants:
            for assertion in variant.assertions:
                if assertion.fact_id not in facts:
                    raise ValueError(f"unknown assertion fact_id: {assertion.fact_id}")
                if any((p.source_id, p.source_hash) != lineage for p in assertion.provenance):
                    raise ValueError("assertion provenance points outside run source")
        return self


def _status(values: list[GateStatus]) -> GateStatus:
    if GateStatus.FAIL in values:
        return GateStatus.FAIL
    if GateStatus.REVIEW_REQUIRED in values:
        return GateStatus.REVIEW_REQUIRED
    return GateStatus.PASS


def _payload(a: FinancialFact | FinancialAssertion) -> tuple[object, ...]:
    return (a.value, a.unit, a.period, a.modality, a.condition, a.direction)


def _details(fact: FinancialFact, assertion: FinancialAssertion) -> tuple[str, ...]:
    return tuple(field for field in ("value", "unit", "period", "modality", "condition", "direction")
                 if getattr(fact, field) != getattr(assertion, field))


def _ref_keys(refs: tuple[ProvenanceRef, ...]) -> frozenset[str]:
    return frozenset(ref.canonical_json() for ref in refs)


def evaluate_consistency(bundle: ConsistencyBundle) -> dict[str, object]:
    """Fail closed; return per-branch findings and only target-local repair hints.

    Does not modify output texts, source facts, provenance, or sibling branches.
    No semantic comparison of arbitrary native format text is claimed.
    """
    facts = {fact.fact_id: fact for fact in bundle.facts}
    variants = {(v.audience, v.output_format): v for v in bundle.variants}
    missing = sorted(BRANCHES - set(variants), key=lambda p: (p[0].value, p[1].value))
    findings: list[dict[str, object]] = []
    proposed_repairs: list[dict[str, str]] = []
    statuses: list[GateStatus] = [GateStatus.REVIEW_REQUIRED] if missing else []
    seen_for_fact: dict[str, list[tuple[VariantAssertions, FinancialAssertion]]] = defaultdict(list)

    for (audience, fmt), variant in sorted(variants.items(), key=lambda t: (t[0][0].value, t[0][1].value)):
        for gate, state in sorted(variant.upstream_gates.items()):
            statuses.append(state)
            if state != GateStatus.PASS:
                findings.append({
                    "code": "UPSTREAM_GATE_NOT_PASS",
                    "decision": state.value,
                    "job_id": variant.job_id,
                    "audience": audience.value,
                    "format": fmt.value,
                    "gate": gate,
                })
        indexed = {assertion.fact_id: assertion for assertion in variant.assertions}
        for fact_id, fact in sorted(facts.items()):
            assertion = indexed.get(fact_id)
            if assertion is None:
                if fact.required_for_all:
                    statuses.append(GateStatus.REVIEW_REQUIRED)
                    findings.append({
                        "code": "REQUIRED_FACT_OMITTED",
                        "decision": GateStatus.REVIEW_REQUIRED.value,
                        "job_id": variant.job_id,
                        "audience": audience.value,
                        "format": fmt.value,
                        "fact_id": fact_id,
                    })
                # Optional omissions are semantically permissible in short formats.
                continue
            seen_for_fact[fact_id].append((variant, assertion))
            if fact.source_gate != GateStatus.PASS:
                # Do not promote an ambiguous source into a claim PASS, even if
                # all nine outputs repeat the same extracted string.
                status = fact.source_gate
                statuses.append(status)
                findings.append({
                    "code": "SOURCE_FACT_GATE_NOT_PASS",
                    "decision": status.value,
                    "job_id": variant.job_id,
                    "fact_id": fact_id,
                })
            if _ref_keys(assertion.provenance) != _ref_keys(fact.provenance):
                statuses.append(GateStatus.REVIEW_REQUIRED)
                findings.append({
                    "code": "ASSERTION_SOURCE_REF_MISMATCH",
                    "decision": GateStatus.REVIEW_REQUIRED.value,
                    "job_id": variant.job_id,
                    "fact_id": fact_id,
                })
            changed = _details(fact, assertion)
            if changed:
                status = (
                    GateStatus.FAIL if fact.materiality in {Materiality.CRITICAL, Materiality.MATERIAL}
                    else GateStatus.REVIEW_REQUIRED
                )
                statuses.append(status)
                findings.append({
                    "code": "CLAIM_SOURCE_CONTRADICTION",
                    "decision": status.value,
                    "job_id": variant.job_id,
                    "audience": audience.value,
                    "format": fmt.value,
                    "fact_id": fact_id,
                    "mismatched_fields": list(changed),
                })
                proposed_repairs.append({
                    "job_id": variant.job_id,
                    "fact_id": fact_id,
                    "reason": "Re-check only this output against validated source value/qualifiers; never rewrite siblings.",
                    "fresh_recheck_required": "true",
                })

    for fact_id, observed in sorted(seen_for_fact.items()):
        if len({_payload(assertion) for _, assertion in observed}) > 1:
            statuses.append(GateStatus.FAIL if facts[fact_id].materiality in {
                Materiality.CRITICAL, Materiality.MATERIAL
            } else GateStatus.REVIEW_REQUIRED)
            findings.append({
                "code": "CROSS_OUTPUT_CONTRADICTION",
                "decision": statuses[-1].value,
                "fact_id": fact_id,
                "observed_job_ids": sorted(variant.job_id for variant, _ in observed),
                "distinct_assertion_count": len({_payload(assertion) for _, assertion in observed}),
            })
    for fact in bundle.facts:
        if fact.source_gate != GateStatus.PASS:
            statuses.append(fact.source_gate)
            if not seen_for_fact.get(fact.fact_id):
                findings.append({
                    "code": "UNVERIFIED_SOURCE_FACT",
                    "decision": fact.source_gate.value,
                    "fact_id": fact.fact_id,
                })
    final_status = _status(statuses) if statuses else GateStatus.REVIEW_REQUIRED
    return {
        "schema_version": "cross_output_report.v1",
        "evaluator_version": VERSION,
        "run_id": bundle.run_id,
        "source_id": bundle.source.source_id,
        "source_hash": bundle.source.source_hash,
        "source_ledger_version": bundle.source_ledger_version,
        "status": final_status.value,
        "observed_branches": len(variants),
        "expected_branches": len(BRANCHES),
        "missing_branches": [{"audience": a.value, "format": f.value} for a, f in missing],
        "findings": findings,
        "targeted_repairs": proposed_repairs,
        "evidence_class": "STRUCTURED_ASSERTION_DIAGNOSTIC_ONLY",
        "source_original_claim_extraction_observed": False,
        "llm_judge_observed": False,
        "human_gold_eligible": False,
        "production_ready": False,
    }
