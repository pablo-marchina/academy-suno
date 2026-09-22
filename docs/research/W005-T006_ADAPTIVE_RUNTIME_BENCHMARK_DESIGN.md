# W005-T006 — Adaptive runtime benchmark / experiment design

`TASK_ID: W005-T006`
`ATTEMPT_ID: A01`
`DESIGN_DATE: 2026-09-22`
`EXECUTION_STATUS: DESIGNED_NOT_EXECUTED`

## Purpose

Provide the reproducible evidence plan required to decide provider/model/prompt/retrieval/repair/budget routing without promoting a technology by preference. This extends the bounded W004 provider comparison into an Academy-representative, hard-gate-preserving experiment.

## Hypotheses

- H1: at least one adaptive/rule-based routing policy can improve the cost/latency/reliability frontier versus a fixed W004-style route while preserving critical hard gates.
- H2: provider/model superiority is workload-slice dependent rather than globally ordered.
- H3: bounded fallback/repair can increase successful completion under transient provider failures without unacceptable retry amplification.
- H4: if H1 is not supported, the deterministic static/rule champion remains valid and the learned router stays unpromoted.

No hypothesis permits compensating a critical hard-gate failure with lower cost or latency.

## Experimental unit and corpus

Primary unit: one Academy branch = `(source_document, audience, format)`.

Required coverage per accepted source document:

- all `3 audiences × 3 formats = 9/9` branches;
- source/numeric/entity/date preservation slices;
- short vs long source context where available;
- narrative vs table/dense-financial slices where available;
- at least one known ambiguity/negative-control source case;
- repair-triggering cases when a reproducible hard/quality failure exists.

Reuse W004 artifacts only as DEVELOPMENT/baseline evidence. Expand beyond the four-task T007-A05 comparison before any production preference. Preserve DEV / CALIBRATION / HELD_OUT separation when the corpus size permits; do not relabel automated calibration as human gold.

## Candidate matrix

### Static model/provider champions

1. Groq `openai/gpt-oss-20b` — W004 baseline.
2. Groq `openai/gpt-oss-120b` — W004 baseline.
3. At least two current OpenAI production capability/cost points.
4. Anthropic `claude-sonnet-5` plus one stronger current challenger if accessible.
5. Google `gemini-3.8-flash` plus one stable/appropriate higher-capability challenger if accessible.

Exact IDs are refreshed immediately before execution and hashed into the manifest.

### Routing-policy challengers

A. fixed single candidate;
B. deterministic workload rules;
C. bounded cheap→strong cascade / targeted repair;
D. provider-managed auto-routing when reproducibly available;
E. Academy constrained adaptive router in shadow mode first.

### Orthogonal policy knobs

Prompt variant, retrieval profile, service tier/budget and repair policy are versioned factors. Avoid a full factorial explosion in the first pass: screen model/provider candidates under one frozen prompt/eval contract, then focus combinations only on non-dominated candidates.

## Preflight

For every candidate record:

- provider/model exact ID and lifecycle status;
- credential/access result without leaking secrets;
- context/output limits and structured-output capability;
- service tier and account/project rate limits;
- official pricing snapshot URL/date/hash;
- deterministic schema contract preflight;
- provider request ID availability;
- timeout/cancellation behavior;
- known retryable status codes;
- telemetry fields available.

A candidate that cannot satisfy mandatory capability/security requirements is `INELIGIBLE`, not scored lower and averaged in.

## Frozen run configuration

Persist one manifest per experiment run containing:

- git commit SHA and dataset hash;
- prompt/template hashes;
- evaluator/policy/retrieval/repair versions;
- exact provider/model IDs and service tiers;
- temperature/reasoning/thinking settings where configurable;
- max output/deadline/retry/fallback budgets;
- price-sheet snapshots and retrieval timestamps;
- random seed where the provider honors one;
- routing-policy hash and rollout mode;
- environment/runtime versions.

## Repetitions and uncertainty

Start each probabilistic cell with `R >= 3` independent repetitions. Increase repetitions for cells whose variance materially affects the decision until confidence-interval width / rank stability stops changing the Pareto conclusion or the cost of additional sampling exceeds decision value. Record raw observations; never report only averages.

For binary hard-gate outcomes report counts and exact observed rate; **zero observed violations is required for promotion but is not evidence of zero true failure probability**. For continuous metrics report median/p50 plus p95/p99 where sample size supports them, and confidence intervals/effect sizes when valid.

## Metrics

### Non-compensatory hard gates

- source trust / citation binding;
- critical factual/numeric/entity/date preservation;
- policy/compliance invariants;
- schema validity;
- tenant/workspace authorization isolation in the defined integration scope;
- provenance / branch identity / lossless 9/9 join.

Promotion condition for observed benchmark: `critical hard-gate violations = 0`.

### Quality sensors

- existing W004 quality score components;
- preservation pass/fail;
- numeric preservation;
- required-concept preservation;
- readability/jargon/audience sensors with current evidence labels;
- later human preference/calibration when PROD-008 evidence exists.

Audience thresholds remain diagnostic until stronger evidence is integrated.

### Latency

- queue wait;
- provider request latency;
- TTFT where available;
- end-to-end branch latency;
- end-to-end 3×3 run latency;
- p50/p95/p99 when sample size permits.

### Reliability

- request success rate;
- retry count and retry success;
- fallback count/rate;
- timeout/cancel rate;
- provider capacity/rate-limit errors;
- hard-gate rejection rate;
- repair attempt and repair acceptance rate;
- circuit-open events.

### Cost / usage

- input/output/reasoning/cache token usage as reported;
- versioned `estimated_cost` from official price snapshot;
- provider-billed amount separately when available;
- cost per accepted branch and accepted 3×3 run;
- retry/repair/fallback incremental cost.

Do not use synthetic cost as if it were billed cost.

## Fault-injection scenarios

Run against an adapter/test harness so provider credentials are not required for every injected failure:

1. 429 with `Retry-After`;
2. transient 5xx;
3. explicit capacity failure (including Groq Flex-style 498 where applicable);
4. connection/read timeout;
5. malformed/schema-incompatible output;
6. unavailable/retired candidate in catalog;
7. open circuit / provider degraded state;
8. cache hit vs miss when measurable;
9. pricing snapshot changed between policy versions;
10. stale policy references a disabled candidate.

Expected behavior is deterministic and asserted before live-provider runs.

## Retry / fallback assertions

- non-retryable auth, invalid request, policy, tenant and deterministic schema/config failures do not blind-retry;
- retryable failures respect a bounded attempt budget and jittered backoff;
- one subsystem owns retries to avoid nested multiplicative amplification;
- fallback requires an eligible capability-equivalent candidate;
- fallback never bypasses post-generation hard gates;
- end-to-end deadline budget decreases across attempts;
- repair count is capped and every repair receives fresh evaluation.

## Routing experiment phases

### Phase 0 — adapter correctness

Run deterministic fixtures and all fault injections; require 100% expected control-flow assertions.

### Phase 1 — static candidate benchmark

Same corpus, prompts, evals and budgets for every eligible model/provider. Produce raw metrics and Pareto frontier. No router training yet.

### Phase 2 — deterministic rules/cascade

Use only DEV/CALIBRATION evidence to define routing features/rules. Compare against the safest non-dominated static champion on HELD_OUT.

### Phase 3 — learned/contextual challenger in shadow

Features may include audience/format, source length/complexity indicators, risk class, historical route health, remaining budget, provider availability and prior deterministic sensor outputs that do not leak held-out target labels. Shadow decisions have no recipient impact.

### Phase 4 — bounded canary exploration

Only after Phase 3 is non-dominated and protocol/security review passes. Explore exclusively among candidates that already satisfy eligibility. Use stable assignment and an explicit experiment budget. Any critical hard-gate failure triggers stop/rollback.

## Analysis and decision rules

1. Remove `INELIGIBLE` candidates from optimization; preserve rejection reason.
2. Any critical hard-gate violation blocks promotion of that policy/version pending root cause and rerun.
3. Compute quality/cost/latency/reliability trade-offs on remaining candidates; expose Pareto frontier rather than an artificial universal score.
4. A router is promotable only if, on HELD_OUT, it is not materially worse on quality/factual preservation and provides an operationally meaningful improvement on at least one target dimension without unacceptable reliability loss.
5. If confidence intervals overlap / sample is insufficient / improvement is marginal, return `NO_PREFERENCE` or `PENDING_EVIDENCE`.
6. Re-run after material model revision, provider retirement, price change, evaluator change, corpus shift or routing-policy change.

No absolute latency/cost/quality target is invented here; T009/T010 may establish evidence-backed thresholds.

## Raw result schema

Each branch attempt should emit at minimum:

```json
{
  "experiment_id": "...",
  "run_id": "...",
  "branch_id": "...",
  "tenant_test_scope": "...",
  "policy_version": "...",
  "route_decision_id": "...",
  "candidate_catalog_version": "...",
  "provider": "...",
  "request_model": "...",
  "response_model": "...",
  "service_tier": "...",
  "prompt_version": "...",
  "retrieval_version": "...",
  "repair_policy_version": "...",
  "exploration_mode": "offline|shadow|canary|active",
  "attempt_index": 0,
  "latency_ms": {"queue": null, "ttft": null, "provider": null, "end_to_end": null},
  "usage": {"input_tokens": null, "output_tokens": null, "cached_input_tokens": null, "reasoning_tokens": null},
  "cost": {"currency": "USD", "estimated": null, "billed": null, "pricing_snapshot": "..."},
  "retry": {"count": 0, "reasons": []},
  "fallback_chain": [],
  "hard_gates": {},
  "quality_metrics": {},
  "accepted": false,
  "error_class": null,
  "provider_request_id": null
}
```

Sensitive prompt/document/output content should be stored only under the product's approved evidence/security policy; telemetry defaults to hashes/IDs and redacted structured metrics.

## Required outputs from future execution

- frozen candidate manifest + hashes;
- raw JSONL/Parquet-equivalent observations;
- price snapshots;
- static candidate Pareto report;
- fault-injection report;
- shadow/canary routing report if reached;
- bootstrap/CI or appropriate uncertainty report;
- `LOCK | NO_PREFERENCE | PENDING_EVIDENCE` decision with reversal conditions.

## Stopping rule

Stop an experimental round when:

- all relevant hard-gate/fault scenarios have coverage;
- additional repetitions no longer change the material Pareto conclusion within the declared uncertainty;
- no newly added eligible candidate changes the frontier;
- remaining uncertainty is explicitly classified and either requires new external/human evidence or is too small to change the current decision.

## Relationship to W005 fan-in

- T004 supplies security/tenancy/provider data constraints.
- T005 supplies stronger eval/calibration methodology.
- T007 supplies observability design.
- T009 supplies cross-cutting benchmark/statistical methodology.
- T010 integrates the architecture and may refine thresholds/candidate scope.
- T013 determines developer-platform/toolchain implications.

This design intentionally leaves provider/model/gateway winner selection open until those inputs and representative measurements exist.
