from __future__ import annotations

import re
from typing import Any

from suno_content.domain import GateStatus

from .models import FactualFinding
from .normalization import (
    extract_dates,
    extract_direction,
    extract_numbers,
    extract_periods,
    extract_percentages,
    extract_scale_words,
    fold,
    has_explicit_range,
    has_modality,
    has_negation,
    round_half_up,
)

_CODE_META: dict[str, tuple[str, GateStatus, bool, str]] = {
    "FACT_NUMERIC_MAGNITUDE_MISMATCH": ("CRITICAL", GateStatus.FAIL, True, "CONTRADICTED"),
    "FACT_SCALE_UNIT_MISMATCH": ("CRITICAL", GateStatus.FAIL, True, "CONTRADICTED"),
    "FACT_PERIOD_MISMATCH": ("CRITICAL", GateStatus.FAIL, True, "CONTRADICTED"),
    "FACT_ENTITY_ROLE_SWAP": ("CRITICAL", GateStatus.FAIL, True, "CONTRADICTED"),
    "FACT_DIRECTION_MISMATCH": ("CRITICAL", GateStatus.FAIL, True, "CONTRADICTED"),
    "FACT_NEGATION_INVERSION": ("CRITICAL", GateStatus.FAIL, True, "CONTRADICTED"),
    "FACT_MODALITY_PROMOTION": ("CRITICAL", GateStatus.FAIL, True, "CONTRADICTED"),
    "FACT_ATTRIBUTION_ERROR": ("CRITICAL", GateStatus.FAIL, True, "CONTRADICTED"),
    "FACT_TABLE_ROLE_MISMATCH": ("CRITICAL", GateStatus.FAIL, True, "CONTRADICTED"),
    "FACT_UNSUPPORTED_CAUSAL_CLAIM": ("ERROR", GateStatus.FAIL, False, "UNSUPPORTED"),
    "FACT_SOURCE_EXTRACTION_AMBIGUOUS": ("ERROR", GateStatus.REVIEW_REQUIRED, True, "UNVERIFIABLE"),
    "FACT_RETRIEVAL_MISS_REVIEW": ("ERROR", GateStatus.REVIEW_REQUIRED, False, "UNVERIFIABLE"),
}


def _spans(case: dict[str, Any]) -> list[dict[str, Any]]:
    return list(case.get("source", {}).get("spans", []))


def _evidence_ids(case: dict[str, Any]) -> tuple[str, ...]:
    return tuple(s.get("span_id") for s in _spans(case) if s.get("span_id"))


def _source_text(case: dict[str, Any]) -> str:
    return "\n".join(str(s.get("text", "")) for s in _spans(case))


def _finding(case: dict[str, Any], code: str) -> FactualFinding:
    severity, decision, hard_gate, support = _CODE_META[code]
    return FactualFinding(
        fixture_id=case.get("id"),
        failure_code=code,
        severity=severity,
        decision=decision,
        hard_gate=hard_gate,
        support_status=support,
        evidence_span_ids=_evidence_ids(case),
    )


def _pass(case: dict[str, Any]) -> FactualFinding:
    return FactualFinding(
        fixture_id=case.get("id"),
        failure_code=None,
        severity="INFO",
        decision=GateStatus.PASS,
        hard_gate=False,
        support_status="SUPPORTED",
        evidence_span_ids=_evidence_ids(case),
    )


def _source_is_ambiguous(case: dict[str, Any]) -> bool:
    source = case.get("source", {})
    source_trust = source.get("source_trust", {})
    if source_trust.get("status") in {"REVIEW_REQUIRED", "FAIL"}:
        return True
    return any(str(s.get("extraction_confidence", "")).upper() == "LOW" for s in _spans(case))


def _retrieval_miss(case: dict[str, Any]) -> bool:
    retrieval = case.get("retrieval_fixture")
    if not isinstance(retrieval, dict):
        return False
    candidates = retrieval.get("candidate_evidence_span_ids") or []
    known = retrieval.get("known_relevant_span_ids") or []
    return not candidates and bool(known)


def _table_role_mismatch(case: dict[str, Any], output: str) -> bool:
    table_spans = [s for s in _spans(case) if isinstance(s.get("table"), dict)]
    if not table_spans:
        return False
    out_folded = fold(output)
    out_numbers = extract_numbers(output)
    if not out_numbers:
        return False
    for numeric in out_numbers:
        matching_cells = []
        for span in table_spans:
            values = extract_numbers(str(span.get("text", "")))
            if any(v.value == numeric.value for v in values):
                matching_cells.append(span)
        for cell in matching_cells:
            row = fold(str(cell.get("table", {}).get("row_header", "")))
            if not row:
                continue
            other_rows = [
                fold(str(s.get("table", {}).get("row_header", "")))
                for s in table_spans
                if s is not cell
            ]
            if any(other and other in out_folded for other in other_rows) and row not in out_folded:
                return True
    return False


def _attribution_error(source: str, output: str) -> bool:
    s, o = fold(source), fold(output)
    external_estimate = "segundo estimativa" in s or "segundo o" in s or "segundo a" in s
    source_denies_guidance = "nao divulgou guidance" in s or "nao forneceu guidance" in s
    output_claims_company_guidance = bool(
        re.search(r"\bcompanhia\b.*\bdivulgou\b.*\bguidance\b", o)
    )
    return external_estimate and source_denies_guidance and output_claims_company_guidance


def _modality_promotion(source: str, output: str) -> bool:
    s, o = fold(source), fold(output)
    source_qualified = has_modality(source) or has_explicit_range(source)
    if not source_qualified:
        return False
    if has_modality(output) or has_explicit_range(output):
        return False
    asserted_future = bool(re.search(r"\b(?:sera|crescer[aá]|atingira|ficara|vai)\b", o))
    source_has_condition = any(
        x in s for x in ("sujeito", "condicionad", "se aprovado", "se ocorrer")
    )
    return asserted_future or source_has_condition or has_explicit_range(source)


def _scale_mismatch(source: str, output: str) -> bool:
    s_scales, o_scales = set(extract_scale_words(source)), set(extract_scale_words(output))
    if not s_scales or not o_scales or s_scales == o_scales:
        return False
    s_nums = {v.value for v in extract_numbers(source)}
    o_nums = {v.value for v in extract_numbers(output)}
    return bool(s_nums & o_nums)


def _period_mismatch(source: str, output: str) -> bool:
    s_dates, o_dates = set(extract_dates(source)), set(extract_dates(output))
    if s_dates and o_dates and s_dates != o_dates:
        return True
    s_periods, o_periods = set(extract_periods(source)), set(extract_periods(output))
    return bool(s_periods and o_periods and s_periods != o_periods)


def _entity_role_swap(source: str, output: str) -> bool:
    s, o = fold(source), fold(output)
    source_pairs = re.findall(
        r"\bcompanhia\s+([a-z0-9_-]+)\s+(?:aprovou|divulgou|anunciou)", s
    )
    output_pairs = re.findall(
        r"\bcompanhia\s+([a-z0-9_-]+)\s+(?:aprovou|divulgou|anunciou)", o
    )
    return bool(source_pairs and output_pairs and set(source_pairs) != set(output_pairs))


def _direction_mismatch(source: str, output: str) -> bool:
    s_dir, o_dir = extract_direction(source), extract_direction(output)
    return bool(s_dir and o_dir and s_dir != o_dir)


def _negation_inversion(source: str, output: str) -> bool:
    if has_negation(source) == has_negation(output):
        return False
    s, o = fold(source), fold(output)
    content = {
        w
        for w in re.findall(r"[a-z0-9]+", s)
        if len(w) >= 5 and w not in {"companhia", "administracao"}
    }
    return sum(1 for w in content if w in o) >= 2


def _unsupported_causality(source: str, output: str) -> bool:
    o = fold(output)
    markers = ("por causa", "devido a", "em razao de", "porque")
    if not any(marker in o for marker in markers):
        return False
    s = fold(source)
    return not any(marker in s for marker in markers)


def _rounding_allows(case: dict[str, Any], source: str, output: str) -> bool:
    policy = case.get("fixture_policy", {}).get("rounding")
    if not isinstance(policy, dict) or policy.get("mode") != "half_up":
        return False
    decimals = policy.get("decimals")
    if not isinstance(decimals, int) or decimals < 0:
        return False
    s_pct, o_pct = extract_percentages(source), extract_percentages(output)
    if len(s_pct) != 1 or len(o_pct) != 1:
        return False
    return round_half_up(s_pct[0], decimals) == o_pct[0]


def _numeric_mismatch(case: dict[str, Any], source: str, output: str) -> bool:
    if _rounding_allows(case, source, output):
        return False
    s_pct, o_pct = extract_percentages(source), extract_percentages(output)
    if s_pct or o_pct:
        return bool(s_pct and o_pct and set(s_pct) != set(o_pct))
    s_nums = [v.value for v in extract_numbers(source)]
    o_nums = [v.value for v in extract_numbers(output)]
    if not s_nums or not o_nums:
        return False
    return not set(o_nums).issubset(set(s_nums))


def evaluate_case(case: dict[str, Any]) -> FactualFinding:
    """Run deterministic checks without consulting oracle labels or a semantic judge."""
    source = _source_text(case)
    output = str(case.get("adversarial_output", ""))
    if _source_is_ambiguous(case):
        return _finding(case, "FACT_SOURCE_EXTRACTION_AMBIGUOUS")
    if _retrieval_miss(case):
        return _finding(case, "FACT_RETRIEVAL_MISS_REVIEW")
    if _table_role_mismatch(case, output):
        return _finding(case, "FACT_TABLE_ROLE_MISMATCH")
    if _attribution_error(source, output):
        return _finding(case, "FACT_ATTRIBUTION_ERROR")
    if _modality_promotion(source, output):
        return _finding(case, "FACT_MODALITY_PROMOTION")
    if _scale_mismatch(source, output):
        return _finding(case, "FACT_SCALE_UNIT_MISMATCH")
    if _period_mismatch(source, output):
        return _finding(case, "FACT_PERIOD_MISMATCH")
    if _entity_role_swap(source, output):
        return _finding(case, "FACT_ENTITY_ROLE_SWAP")
    if _direction_mismatch(source, output):
        return _finding(case, "FACT_DIRECTION_MISMATCH")
    if _negation_inversion(source, output):
        return _finding(case, "FACT_NEGATION_INVERSION")
    if _unsupported_causality(source, output):
        return _finding(case, "FACT_UNSUPPORTED_CAUSAL_CLAIM")
    if _numeric_mismatch(case, source, output):
        return _finding(case, "FACT_NUMERIC_MAGNITUDE_MISMATCH")
    return _pass(case)
