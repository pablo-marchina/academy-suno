# W004 blind annotation operator — human handoff

This operator reduces the friction of collecting the two independent primary streams required by W004-T005. It does not create human evidence by itself and must never be used to auto-label, clone one human into two streams, or expose target/evaluator/provider information.

## Independence rules

Use two genuinely independent humans. Give each person a separate workspace/session and a distinct pseudonymous annotator-id such as human-a and human-b. Do not use passwords, emails, or other secrets. PRIMARY_A must not see PRIMARY_B labels or notes, and vice versa, until both exports are complete and frozen.

Neither primary may receive requested targets, evaluator predictions/scores, generator/model/prompt identity, peer annotations, or held-out material. Adjudication is a separate later stage; do not reuse a primary session as an adjudication session.

## Validate the frozen handoff

From repository root:

    python app/annotation/operator.py validate

Expected: status PASS and item_count 36. The command reads only the fixed W004-T002 blind bank and fails closed on contract drift, forbidden fields, held-out material, or wrong population size.

## Human A

    python app/annotation/operator.py init --session .annotation_work/primary_a/session.json --role PRIMARY_A --annotator-id human-a
    python app/annotation/operator.py annotate --session .annotation_work/primary_a/session.json

Repeat annotate until all 36 items are complete. Check progress with:

    python app/annotation/operator.py status --session .annotation_work/primary_a/session.json

Then export:

    python app/annotation/operator.py export --session .annotation_work/primary_a/session.json --output .annotation_work/primary_a/annotations_primary_a.jsonl

Export is refused until all 36 records exist exactly once. It writes JSONL plus a provenance sidecar with session ID, pseudonymous annotator ID, role, blind-bank hash, item count, and export hash.

## Human B

Use a separate workspace/session and different pseudonymous ID:

    python app/annotation/operator.py init --session .annotation_work/primary_b/session.json --role PRIMARY_B --annotator-id human-b
    python app/annotation/operator.py annotate --session .annotation_work/primary_b/session.json
    python app/annotation/operator.py export --session .annotation_work/primary_b/session.json --output .annotation_work/primary_b/annotations_primary_b.jsonl

Freeze both exports before comparing labels or beginning adjudication.

## Import a compliant external primary stream

If a human used another form/interface, initialize an empty matching role + annotator session and import the complete stream:

    python app/annotation/operator.py import --session .annotation_work/primary_a/session.json --input /path/to/annotations_primary_a.jsonl

Import is strict: same 36 frozen item IDs, one record each, matching role, matching pseudonymous annotator ID, schema-compatible values, and no extra/forbidden fields. A PRIMARY_A stream cannot be imported into PRIMARY_B, and streams are never merged.

## Handoff to W004-T005

After both genuinely independent streams are frozen, hand off:

- annotations_primary_a.jsonl plus its provenance sidecar;
- annotations_primary_b.jsonl plus its provenance sidecar.

W004-T005 can then compute pre-adjudication agreement and build the adjudication queue under the existing human-calibration protocol. This operator never exposes held-out data and does not claim that the W004-T005 human-evidence gate is satisfied.
