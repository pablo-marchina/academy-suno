# Capture runbook — target 04:40, hard cap 05:00

This runbook is intentionally operational rather than a success claim. It does not replace the required real recording.

## Before pressing Record

1. Run `python scripts/demo_capture/prepare_capture.py` and confirm it exits `0`.
2. Open `artifacts/demo/capture_preflight.json`; note `repository.head_sha` and `source_document.sha256`.
3. Start the recipient app on `http://127.0.0.1:8765`.
4. Keep a terminal ready at repo root and the browser at the app home page.
5. Use a screen recorder that exposes elapsed time.

## Single take

| Time | Screen/action | Evidence to make visible |
| --- | --- | --- |
| 00:00–00:20 | Terminal: `git rev-parse HEAD`; open preflight manifest | exact SHA, BCB source URL, raw PDF SHA-256 |
| 00:20–00:45 | App home | real interactive UI + `MECHANICS_ONLY`, `DIAGNOSTIC_ONLY`, `PRODUCTION_UNKNOWN` |
| 00:45–01:15 | Paste the text sample below and submit | raw text path, plain-text parser, source hash, SOURCE_READY when gate permits |
| 01:15–02:15 | Return home; enter `artifacts/demo/source_document.pdf`; submit | actual public PDF path, parser/version/confidence, source trust, raw PDF SHA matching preflight |
| 02:15–03:05 | Scroll the result table | all 9 canonical audience × format rows; `MECHANICS_ONLY` on rows |
| 03:05–03:45 | Scroll to integrated evidence / repair panel | persisted FAIL → PASS, different before/after hashes, fresh gates, sibling immutability |
| 03:45–04:20 | Show non-claims/evidence posture | audience thresholds `DIAGNOSTIC_ONLY`; provider quality/latency/cost `PRODUCTION_UNKNOWN/BLOCKED`; production readiness pending |
| 04:20–04:40 | Terminal: show preflight manifest again + stop recording | bind ending to same SHA/source hash and stop before 05:00 |

### Text sample for the raw-text path

Use this explicit demo-only text; do not represent it as provider or human evidence:

```text
Demonstração mecânica de ingestão: receita líquida de R$ 100, caixa de R$ 50 e dívida de R$ 20 no período de referência.
```

## Narration anchors

Keep these distinctions explicit:

- “`SOURCE_READY/PASS` aqui é o gate de ingestão, não quality PASS de provider e não production readiness.”
- “O 3×3 é `MECHANICS_ONLY`; estes previews não são outputs de provider.”
- “Thresholds de audiência permanecem `DIAGNOSTIC_ONLY` porque não há duas streams humanas independentes integradas.”
- “Qualidade, latência, uso e custo de provider real continuam `PRODUCTION_UNKNOWN/BLOCKED`.”
- “A linhagem FAIL → repair → PASS é o artefato persistido do smoke integrado, não uma animação fabricada para esta gravação.”

## Overrun cuts

If elapsed time reaches 04:20 before the non-claims section is complete, cut narration, not evidence. Never cut:

1. the public PDF provenance/hash;
2. the 3×3 view;
3. the persisted FAIL → repair → PASS panel;
4. the explicit evidence/non-claim labels.

Stop the recording before `05:00` even if narration is incomplete, then recapture from the start.
