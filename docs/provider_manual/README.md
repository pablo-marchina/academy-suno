# Manual provider evidence path — W004-T010

This path turns the integrated W004-T004 provider probe into a **manual-only**, credential-safe action that can later produce versioned observed mechanics evidence for W004-T007. Preparing or successfully running this workflow does **not** establish provider/model quality or a provider preference.

## Safety and evidence contract

- `.github/workflows/provider-manual-evidence.yml` has only `workflow_dispatch`; there is no push, pull-request, schedule, or automatic provider trigger.
- The API credential is read only from the GitHub secret `PROVIDER_API_KEY` and is passed to the existing T004 harness by environment-variable name. It is never a CLI argument, output field, artifact field, or step summary value.
- No `set -x` is used. The wrapper and importer never print environment variables.
- Missing `PROVIDER_API_KEY` is a valid operational outcome but produces `BLOCKED_NO_CREDENTIAL`, `observed_run: false`, and `mechanics_eligible_for_t007: false`. A green workflow means the manual path executed; it is **not** proof that a provider run occurred. Read the artifact status.
- Provider, wire protocol, exact model, provider-visible model version/date, endpoint, and capture time are required provenance for comparable observed mechanics.
- Cost is eligible only when provider-reported usage is observed and the T004 pricing guard marks a versioned snapshot as `official_provider_pricing` with source URL, retrieval/effective time, and currency. Synthetic/unknown pricing is rejected for comparison.
- Response content is not persisted by this mechanics path; the existing harness stores only SHA-256 and byte count.
- Content-quality evidence remains separate. `full_provider_comparison_eligible` is always `false` here; W004-T007 must join these mechanics with valid human/source quality evidence.

## One controlled action

1. Configure the protected GitHub environment `provider-observed-evidence` as appropriate for the repository's approval policy.
2. Add an authorized environment/repository secret named `PROVIDER_API_KEY`.
3. If cost evidence is required, prepare a repository-visible pricing snapshot that satisfies the existing T004 official-pricing provenance contract. Do not put credentials in it.
4. Open **Actions → Provider manual observed evidence → Run workflow**.
5. Supply provider, protocol, exact model, model version/date, endpoint, prompt file, and optional pricing snapshot path.
6. Review the step summary and download the `provider-observed-evidence-<run>-<attempt>` artifact. Do not interpret workflow success by itself as observed provider evidence.

The default prompt file `experiments/provider_manual/inputs/smoke_prompt.txt` is only a mechanics smoke input. W004-T007 must use a predeclared representative/comparable input set for any provider comparison.

## Artifact layers

`provider-probe.json` is the existing `provider-probe-v1` T004 output. `provider-evidence.json` is the stable `provider-observed-evidence-v1` export used by this task. `t007-import.json` is an audit/import envelope with explicit `mechanics_comparable` and findings.

The JSON schema is documented at `docs/provider_manual/provider-observed-evidence-v1.schema.json`. The executable validator is `experiments/provider_manual/provider_evidence.py`; it is stricter than the documentation-only JSON Schema for comparison eligibility.

## Local no-secret proof

A safe no-secret path can be exercised without network access:

```bash
unset PROVIDER_API_KEY
python experiments/provider_manual/run_manual_provider.py \
  --provider example \
  --protocol openai_responses \
  --model example-model \
  --model-version 2026-09-17 \
  --endpoint https://example.invalid/v1/responses \
  --prompt-file experiments/provider_manual/inputs/smoke_prompt.txt \
  --probe-output /tmp/provider-probe.json \
  --evidence-output /tmp/provider-evidence.json
```

Expected evidence posture: `status=BLOCKED_NO_CREDENTIAL`, no HTTP latency/usage/cost, `observed_run=false`, and T007 mechanics eligibility false. The T004 harness checks the credential before constructing or sending a request.

## Import/validation behavior

Strict validation (intended before comparable T007 mechanics input):

```bash
python experiments/provider_manual/import_provider_evidence.py --input provider-evidence.json
```

It exits non-zero for blocker-only, incomplete, synthetic-pricing, missing-version, missing-usage/cost, missing-fingerprint, or secret-like evidence. `--audit-only` permits those artifacts to be retained as audit evidence while keeping `mechanics_comparable=false`.

This separation is deliberate: **auditability is not comparability**, and mechanics comparability is still not content-quality proof.
