from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from suno_content.domain import AudienceLevel, OutputFormat  # noqa: E402
from suno_content.evals.audience import evaluate_audience_features, load_ontology  # noqa: E402

ONTOLOGY = load_ontology(ROOT / "data" / "ontology" / "finance_ptbr_v001.json")

CASES = {
    "explained_beginner": (
        "O EBITDA é uma medida do resultado operacional antes de juros, impostos, depreciação e amortização. "
        "Pense como uma lente para observar a operação antes desses efeitos.",
        {"corp:ebitda"},
    ),
    "jargon_stuffing": ("EBITDA EBITDA LAJIDA EBITDA CAPEX EBITDA.", {"corp:ebitda"}),
    "sentence_chopping": ("Juros. Caem. Preços. Sobem. Crédito. Muda.", set()),
    "concept_removal": ("A economia está mais calma. Há espaço para crescer.", {"macro:output_gap"}),
}


def main() -> None:
    payload = {}
    for name, (text, required) in CASES.items():
        vector = evaluate_audience_features(
            text,
            audience=AudienceLevel.BEGINNER,
            output_format=OutputFormat.ARTICLE,
            ontology=ONTOLOGY,
            required_concept_ids=required,
        )
        payload[name] = vector.model_dump(mode="json")
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
