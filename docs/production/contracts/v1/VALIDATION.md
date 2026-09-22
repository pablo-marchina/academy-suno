# W006-T001-A02 contract/registry validation evidence

`VALIDATION_SCOPE: docs/production/contracts/v1 + docs/decisions/DECISION_RESEARCH_REGISTRY.v1.json`  
`SCHEMA_DRAFT: JSON Schema Draft 2020-12`  
`REFERENCE_VALIDATOR_OBSERVED: python jsonschema 4.26.0`

## Validation results

| Check | Result | Evidence |
|---|---|---|
| Core schema structural validity | PASS | `Draft202012Validator.check_schema` |
| Registry schema structural validity | PASS | `Draft202012Validator.check_schema` |
| Registry instance against registry schema | PASS | Draft 2020-12 validation |
| Canonical IDs unique | PASS | 16 records / 16 unique IDs |
| Canonical refs unique | PASS | 16 records / 16 unique `dr://DR-####` refs |
| Source inventory | PASS | 16 registry sources matched current `docs/decisions/research/` inventory and recorded Git blob SHAs |
| Legacy collision handling | PASS | bare `DR-0001` is `AMBIGUOUS_REQUIRES_SOURCE`; each source-qualified alias resolves uniquely |
| Unknown DR reference | PASS (rejected) | resolver raises unknown-reference failure |
| Protected resource missing provenance | PASS (rejected) | required field |
| Protected resource missing tenant identity | PASS (rejected) | `org_id`/`workspace_id` required |
| Cursor attempts tenant selection | PASS (rejected) | cursor has only opaque token + revision and `additionalProperties=false` |
| Event missing transition identity | PASS (rejected) | `transition_id` required |
| Malformed event revision | PASS (rejected) | integer revision contract |
| Evidence-gated winner introduced | PASS (none) | contracts remain provider/runtime/parser/evaluator/backend/framework/package-manager neutral |
| Protocol-governed/canonical coordination mutation | PASS by task file set | no such path is an owned output; validator `--base-ref` enforces denylist |

## Reproduction

From repository root in an environment with a Draft 2020-12-capable `jsonschema` implementation:

```bash
python docs/production/contracts/v1/validate_contracts.py --base-ref main
```

The script also recomputes each registered Decision Research source Git blob SHA from file bytes, verifies alias targets, exercises ambiguous/unknown resolution, and checks the changed-file set against the protocol/canonical denylist.

## Negative-case expectation

All negative fixtures are **expected rejections**. A negative fixture becoming valid is a regression and the validator exits non-zero.

## Evidence boundary

This validation proves contract/registry structure and fail-closed reference behavior. It does not prove a production persistence/runtime/parser/provider/evaluator implementation and does not authorize any unresolved technology choice.
