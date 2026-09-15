from __future__ import annotations

from pathlib import Path

from suno_content.factual import evaluate_case
from suno_content.factual.corpus import read_jsonl

ROOT = Path(__file__).resolve().parents[2]
CORPUS = ROOT / "tests/fixtures/adversarial/factual_v001.jsonl"


def test_factual_v001_matches_frozen_oracle_fields_without_reading_expected_labels_for_decision():
    rows = read_jsonl(CORPUS)
    assert len(rows) == 13
    for row in rows:
        finding = evaluate_case(row)
        expected = row["expected"]
        assert finding.failure_code == expected["failure_code"], row["id"]
        assert finding.severity == expected["severity"], row["id"]
        assert finding.decision.value == expected["decision"], row["id"]
        assert finding.support_status == expected["support_status"], row["id"]
        if expected["severity"] == "CRITICAL":
            assert finding.hard_gate is True
            assert finding.decision.value == "FAIL"


def test_retrieval_miss_and_source_ambiguity_are_not_collapsed_into_unsupported():
    by_id = {row["id"]: row for row in read_jsonl(CORPUS)}
    ambiguous = evaluate_case(by_id["EXP-C-F11"])
    retrieval = evaluate_case(by_id["EXP-C-F12"])
    unsupported = evaluate_case(by_id["EXP-C-F10"])
    assert ambiguous.failure_code == "FACT_SOURCE_EXTRACTION_AMBIGUOUS"
    assert ambiguous.support_status == "UNVERIFIABLE"
    assert retrieval.failure_code == "FACT_RETRIEVAL_MISS_REVIEW"
    assert retrieval.support_status == "UNVERIFIABLE"
    assert unsupported.failure_code == "FACT_UNSUPPORTED_CAUSAL_CLAIM"
    assert unsupported.support_status == "UNSUPPORTED"


def test_allowed_rounding_control_passes():
    control = next(row for row in read_jsonl(CORPUS) if row["id"] == "EXP-C-C01")
    finding = evaluate_case(control)
    assert finding.failure_code is None
    assert finding.decision.value == "PASS"


def test_exact_date_mismatch_uses_period_failure_code():
    case = {
        "id": "DATE",
        "source": {"spans": [{"span_id": "S1", "text": "A reunião ocorreu em 17/03/2026.", "extraction_confidence": "HIGH"}]},
        "adversarial_output": "A reunião ocorreu em 18/03/2026.",
    }
    finding = evaluate_case(case)
    assert finding.failure_code == "FACT_PERIOD_MISMATCH"
    assert finding.decision.value == "FAIL"


def test_year_is_not_partially_parsed_as_numeric_anchor():
    from suno_content.factual.normalization import extract_numbers

    values = extract_numbers("Em 2026, a margem foi 10,0%.")
    assert [str(item.value) for item in values] == ["2026", "10.0"]


def test_flat_source_trust_review_required_is_supported():
    case = {
        "id": "TRUST",
        "source": {
            "source_trust": "REVIEW_REQUIRED",
            "spans": [{"span_id": "S1", "text": "Taxa de 8%.", "extraction_confidence": "HIGH"}],
        },
        "adversarial_output": "Taxa de 8%.",
    }
    finding = evaluate_case(case)
    assert finding.failure_code == "FACT_SOURCE_EXTRACTION_AMBIGUOUS"
    assert finding.decision.value == "REVIEW_REQUIRED"
