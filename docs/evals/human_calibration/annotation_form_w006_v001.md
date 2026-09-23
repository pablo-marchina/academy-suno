# W006 blind human annotation form v001

Use this form only with a frozen packet produced for `CALIBRATION` or a future post-freeze `HELD_OUT` release evaluation. Do not expose the generation target, evaluator/judge outputs, generator identity, prompt/model/provider, baseline/candidate arm, or the other primary annotation.

## Packet identity

- Packet ID:
- Item ID:
- Source-group ID:
- Partition: `CALIBRATION` / `HELD_OUT`
- Packet SHA-256:
- Output SHA-256:
- Annotator pseudonymous ID:
- Role: `PRIMARY_A` / `PRIMARY_B` / `ADJUDICATOR`
- Rubric version:

## Audience dimensions

Score each dimension `0 / 1 / 2` according to the frozen rubric. Do not infer the requested generation target.

- D1 — Jargon contextualization:
- D2 — Background assumed:
- D3 — Conceptual depth:
- D4 — Content focus:
- D5 — Technicity preservation:

Global audience label: `BEGINNER / INTERMEDIATE / ADVANCED / UNSCORABLE`

If `UNSCORABLE`, reason:

## Non-compensatory checks

- FACTUAL_SOURCE_POLICY: `PASS / FAIL / REVIEW_REQUIRED`
- NUMERIC_ENTITY_DATE: `PASS / FAIL / REVIEW_REQUIRED`
- MATERIAL_CONCEPT_PRESERVATION: `PASS / FAIL / REVIEW_REQUIRED`
- FORMAT_NATIVE_CONTRACT: `PASS / FAIL / NOT_APPLICABLE / REVIEW_REQUIRED`

Confidence: `LOW / MEDIUM / HIGH`

Evidence note limited to the displayed source/output:

## Adjudicator-only

Complete only after both primaries are frozen.

- Primary annotation ref A:
- Primary annotation ref B:
- Adjudication reason:
- Final label: `BEGINNER / INTERMEDIATE / ADVANCED / UNSCORABLE / UNRESOLVED`

An adjudicator must remain blind to generation target, evaluator/judge predictions and baseline/candidate identity. `UNRESOLVED` is valid when evidence is insufficient.
