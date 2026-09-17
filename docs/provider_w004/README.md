# W004 provider/model observed-telemetry harness

This harness exists to collect **mechanics evidence only** for W004-T004. It does not score or compare content quality, and it must not be used to select a provider/model without comparable measured quality data from the downstream W004-T007 comparison.

## Evidence rules

- Provider, protocol, model, model version (when exposed), endpoint and capture timestamp are always explicit.
- Latency is populated only for an actual HTTP attempt. Missing credentials leave latency as `N/A` because no provider call occurred.
- Usage is taken only from provider-reported response metadata. Missing usage stays `N/A`.
- Cost is never invented. It is derived only when provider-reported token usage is present **and** a versioned pricing snapshot declares `kind: official_provider_pricing` plus source URL, retrieval timestamp, effective timestamp/date and currency.
- `synthetic` or unknown pricing is explicitly ineligible as commercial evidence and leaves cost `N/A`.
- Response content is not persisted by default; only byte length and SHA-256 are recorded, preventing mechanics telemetry from masquerading as content-quality evidence.

## Supported request protocols

The initial harness supports `openai_responses` and `anthropic_messages` wire formats using Python's standard library. This is transport coverage, not a provider preference.

## Example invocation

```bash
python experiments/provider_w004/run_provider_probe.py \
  --provider <provider-name> \
  --protocol openai_responses \
  --model <model-id> \
  --model-version <provider-visible-version-or-date> \
  --endpoint <provider-endpoint> \
  --api-key-env <ENV_VAR_NAME> \
  --prompt "Return the word OK." \
  --pricing-snapshot docs/provider_w004/pricing_snapshot.example.json \
  --output experiments/provider_w004/runs/<run-id>.json
```

The example pricing file is deliberately non-commercial. Replace it only with a snapshot copied from an official provider pricing source, preserving source and timestamps.

## Current execution status

The worker runtime used for W004-T004-A01 does not expose provider credentials or an external provider execution channel. Therefore no real provider call was fabricated. The harness is ready for a credentialed runtime; the task result records the external-runtime blocker explicitly.
