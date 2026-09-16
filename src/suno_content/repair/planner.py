from __future__ import annotations

from .models import EvaluationSnapshot, RepairDirective, RepairRequest


_PREFIX_RULES: tuple[tuple[str, tuple[str, str, bool]], ...] = (
    ("SOURCE_", ("RESTORE_SOURCE_LINEAGE", "repair source/provenance mismatch from canonical evidence", True)),
    ("FACTUAL_", ("CORRECT_FACTUAL_CLAIM_FROM_SOURCE", "repair factual mismatch using source-backed values only", True)),
    ("POLICY_", ("REMOVE_OR_REFRAME_POLICY_VIOLATION", "remove unsupported recommendation/escalation while preserving source meaning", True)),
    ("CLAIM_CONTRADICTED", ("REWRITE_CONTRADICTED_CLAIM", "rewrite only the contradicted claim against its evidence", True)),
    ("CLAIM_UNSUPPORTED", ("REMOVE_OR_GROUND_UNSUPPORTED_CLAIM", "remove or ground only the unsupported claim", True)),
    ("REQUIRED_CONCEPT_OMISSION", ("RESTORE_REQUIRED_CONCEPTS", "restore required financial concepts without padding", True)),
    ("UNEXPLAINED_JARGON", ("EXPLAIN_FIRST_USE", "explain required finance terms at first use", True)),
    ("CONTEXTUALIZATION", ("ADD_PRACTICAL_CONTEXT", "add practical context for the flagged concept", True)),
    ("ANALOGY_REQUIRED", ("ADD_TARGETED_ANALOGY", "add one audience-appropriate analogy for the flagged concept", True)),
    ("JARGON_STUFFING", ("REMOVE_GAMING_PATTERN", "remove repeated jargon without deleting required concepts", True)),
    ("ALIAS_STUFFING", ("REMOVE_GAMING_PATTERN", "collapse alias repetition without deleting required concepts", True)),
    ("GLOSSARY_DUMPING", ("INTEGRATE_EXPLANATIONS_IN_CONTEXT", "replace glossary dumping with contextual explanation", True)),
    ("SENTENCE_CHOPPING", ("RESTORE_COHERENT_SENTENCES", "repair readability gaming while preserving meaning", True)),
    ("ACRONYM_HACK", ("EXPAND_AND_EXPLAIN_ACRONYM", "expand/explain acronyms rather than optimizing the surface metric", True)),
    ("RETRIEVAL_MISS", ("REVIEW_EVIDENCE_PIPELINE", "content rewrite cannot repair an evidence retrieval miss", False)),
    ("EXTRACTION_AMBIGUITY", ("REVIEW_EXTRACTION_PIPELINE", "content rewrite cannot repair ambiguous source extraction", False)),
)

_METRIC_RULES: dict[str, tuple[str, str]] = {
    "required_concept_recall": ("RESTORE_REQUIRED_CONCEPTS", "required concept recall is below its local target"),
    "unexplained_jargon_rate": ("EXPLAIN_FIRST_USE", "unexplained jargon rate violates the diagnostic target"),
    "contextualization_rate": ("ADD_PRACTICAL_CONTEXT", "contextualization rate violates the diagnostic target"),
    "analogy_rate": ("ADD_TARGETED_ANALOGY", "analogy coverage violates the diagnostic target"),
}


def _directive_for_code(code: str) -> RepairDirective:
    for prefix, (operation, reason, repairable) in _PREFIX_RULES:
        if code.startswith(prefix):
            return RepairDirective(code, operation, reason, repairable)
    return RepairDirective(
        source_code=code,
        operation="REVIEW_UNMAPPED_FINDING",
        reason="failure code has no approved local repair mapping",
        repairable=False,
    )


def build_repair_request(
    *,
    job_id: str,
    attempt_number: int,
    snapshot: EvaluationSnapshot,
) -> RepairRequest:
    directives: list[RepairDirective] = []
    seen_operations: set[str] = set()

    for code in snapshot.failure_codes:
        directive = _directive_for_code(code)
        if directive.operation not in seen_operations:
            directives.append(directive)
            seen_operations.add(directive.operation)

    metric_triggers: list[str] = []
    for metric in snapshot.metrics:
        if not metric.violated:
            continue
        metric_triggers.append(metric.name)
        rule = _METRIC_RULES.get(metric.name)
        if rule is None:
            continue
        operation, reason = rule
        if operation not in seen_operations:
            directives.append(
                RepairDirective(
                    source_code=f"METRIC:{metric.name}",
                    operation=operation,
                    reason=reason,
                    repairable=True,
                )
            )
            seen_operations.add(operation)

    return RepairRequest(
        job_id=job_id,
        attempt_number=attempt_number,
        before_evaluation_id=snapshot.evaluation_id,
        failure_codes=tuple(snapshot.failure_codes),
        metric_triggers=tuple(metric_triggers),
        directives=tuple(directives),
    )
