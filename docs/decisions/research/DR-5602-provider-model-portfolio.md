# DR-5602 — Provider/model portfolio for adaptive runtime

`TASK_ID: W005-T006`
`ATTEMPT_ID: A01`
`RESEARCH_DATE: 2026-09-22`
`DECISION: NO_OVERALL_PROVIDER_MODEL_PREFERENCE; PENDING_REPRESENTATIVE_BAKEOFF`
`CONFIDENCE: HIGH that a portfolio abstraction is required; LOW that any current provider/model is globally best for Academy Suno`

## Decision question

Which provider/model portfolio should Academy Suno expose to the adaptive runtime, and is current evidence sufficient to select a production default?

## Baseline

W004-T007-A05 observed eight Groq calls across four DEVELOPMENT source-preservation tasks using `openai/gpt-oss-120b` and `openai/gpt-oss-20b`. It found a bounded quality/latency/cost trade-off and explicitly concluded `NO_OVERALL_MODEL_PREFERENCE`. That evidence is a reproducible baseline, not a cross-provider or production workload winner.

## Candidate families for the benchmark

The following are **dated benchmark seeds, not production defaults**. Exact IDs must be refreshed at experiment execution and stored in the run manifest.

| Family | Candidate examples as of 2026-09-22 | Why include | Caveat |
|---|---|---|---|
| Groq | `openai/gpt-oss-20b`, `openai/gpt-oss-120b` | Preserves W004 counterfactual; current Groq docs list both as production models and support strict structured outputs on them | W004 sample is small/bounded; one hosting path does not establish general superiority |
| OpenAI | `gpt-5.6-luna`, `gpt-5.6-terra`, `gpt-5.6-sol` or current comparable production variants | Current catalog spans materially different cost/latency/capability tiers and exposes Standard/Flex/Fast controls | Pricing/service tiers are mutable; Academy workload quality is unmeasured |
| Anthropic | `claude-sonnet-5` plus a stronger current Opus-class challenger where access permits | Current active portfolio adds an independent model family and useful quality/cost counterfactual | Model lifecycle/deprecations require catalog refresh; benchmark not yet run |
| Google Gemini | `gemini-3.8-flash` plus a current higher-capability challenger where stable/available | Current GA Flash model provides another independent provider/capability point; Google also exposes routing primitives | Introductory pricing changes are scheduled; previews must not be silently treated as stable production defaults |

A benchmark MAY add another materially different provider only if it introduces a new cost/capability/reliability frontier rather than redundant volume.

## Criteria

Hard requirements before any route is eligible:

- source/factual/policy/schema/tenant/provenance controls compatible with Academy's deterministic envelope;
- structured output / validation path adequate for typed boundaries, or a deterministic wrapper that fails closed;
- observable model identity, token/usage accounting and request outcome;
- supported model lifecycle state and explicit timeout/rate-limit behavior;
- acceptable data/security controls after T004 integration.

Among eligible candidates compare, without compensating hard failures:

- Academy quality/preservation metrics and later human-calibrated evidence;
- p50/p95/p99 end-to-end latency and TTFT where supported;
- request success/error/retry/fallback rate;
- actual token usage, cache usage and cost from a versioned price sheet;
- rate/capacity behavior;
- operational integration complexity and lock-in.

## Current primary-source snapshot

| Source | Dated observation | Decision implication |
|---|---|---|
| Groq models — https://console.groq.com/docs/models | GPT-OSS 20B/120B remain listed production models with materially different throughput/pricing | Keep both as W004-connected baseline seeds |
| Groq structured outputs — https://console.groq.com/docs/structured-outputs | strict JSON-schema mode is documented for GPT-OSS 20B/120B | Structured-output capability is a positive eligibility signal, not quality proof |
| Groq Flex — https://console.groq.com/docs/flex-processing | Flex offers higher throughput, same on-demand pricing and can fail fast with HTTP 498 on unavailable capacity | Include service tier and 498 fault scenario in routing benchmark |
| OpenAI pricing — https://developers.openai.com/pt-BR/api/docs/pricing | current catalog and service tiers show wide price differences; promotional/current pricing is explicitly time-sensitive | Store price snapshot per run; do not hard-code enduring cost assumptions |
| OpenAI Flex — https://developers.openai.com/pt-BR/api/docs/guides/flex-processing | lower cost trades for longer response / occasional unavailability | Treat service tier as policy variable, not semantic-quality assumption |
| OpenAI Fast mode — https://developers.openai.com/pt-BR/api/docs/guides/fast-mode | low-latency tier exists for supported models | Benchmark latency benefit and incremental cost on Academy workload |
| Anthropic Sonnet 5 — https://www.anthropic.com/news/claude-sonnet-5 | current Sonnet 5 pricing/capability snapshot | Suitable cross-family candidate, not winner evidence |
| Anthropic deprecations — https://docs.anthropic.com/en/docs/about-claude/model-deprecations | active/deprecated/retired states and retirement dates are explicit | Candidate catalog needs lifecycle health and periodic re-evaluation |
| Gemini models — https://ai.google.dev/gemini-api/docs/models | `gemini-3.8-flash` is current stable GA; preview/experimental aliases have weaker stability guarantees | Prefer stable IDs for production benchmark unless a preview is explicitly isolated |
| Gemini 3.8 Flash — https://ai.google.dev/gemini-api/docs/latest-model | current introductory price is explicitly scheduled to change after 2026-12-31 | Cost comparison must bind to execution date and price snapshot |
| Vertex RoutingConfig — https://docs.cloud.google.com/vertex-ai/generative-ai/docs/reference/rpc/google.cloud.aiplatform.v1 | managed automatic routing can prioritize quality, balance, or cost | Managed routing can be a benchmark challenger, not trusted as Academy-safe without post-route gates |

## Findings

1. **Current vendor portfolios move too quickly for a model ID to be architectural truth.** The runtime needs a versioned candidate catalog with lifecycle (`active`, `degraded`, `disabled`, `retiring`), capability, provider/tier, context/output constraints and pricing-snapshot references.
2. **Cost cannot be inferred from a static table alone.** The benchmark must combine observed input/output/cache/reasoning token usage with the exact official price snapshot used for the run, and preserve `estimated_cost` separately from any provider-billed amount.
3. **Service tiers are routing actions.** OpenAI Standard/Flex/Fast and Groq default/Flex-like controls change latency/capacity/cost behavior and should be represented in the route action when supported.
4. **Structured-output support is an eligibility/correctness feature, not a quality score.** Even strict schema adherence does not prove factuality, source faithfulness or audience calibration.
5. **Provider-managed routers are counterfactuals, not authority.** Their decisions remain inside Academy's pre/post hard-gate envelope and need the same telemetry and held-out comparison.
6. **Security/data-handling promotion is intentionally deferred to cross-task fan-in.** T006 must not select a provider before T004/T010 reconcile tenancy, data residency/retention, secrets and deployment constraints.

## Decision

`NO_OVERALL_PROVIDER_MODEL_PREFERENCE` and `PENDING_REPRESENTATIVE_BAKEOFF`.

Carry forward a dated, refreshable candidate portfolio containing at minimum:

- the two W004 Groq GPT-OSS baselines;
- at least two materially different OpenAI capability/cost points when accessible;
- Anthropic Sonnet 5 and, if accessible, a stronger current challenger;
- Gemini 3.8 Flash and, if stable/appropriate, a higher-capability challenger;
- managed auto-routing as a separate policy challenger where it can be invoked reproducibly.

Do not promote a production default until the W005 benchmark runs the same Academy corpus/configuration across candidates and all critical hard gates remain zero-violation in the observed promotion set.

## Benchmark refresh protocol

Immediately before executing the benchmark:

1. query official provider model catalogs and deprecation pages;
2. pin exact model IDs/versions where possible;
3. snapshot official pricing, rate-limit/service-tier docs and retrieval date;
4. record account/project-specific limits separately from published defaults;
5. capability-preflight every candidate with the Academy structured contract;
6. disable retired/unavailable candidates rather than silently substituting them;
7. emit a manifest hash so later reruns can explain portfolio drift.

## Reversal conditions

A production preference can replace `NO_PREFERENCE` only if representative Academy evidence shows a candidate or routing policy is non-dominated and operational/security constraints pass. Reopen any preference after material model revision, retirement, >material pricing change, recurring reliability degradation, changed workload distribution or significant eval regression.

## Traceability

- PROD-005: real provider/model identity and measurable provider abstraction.
- PROD-007: candidate outputs must pass the same hybrid hard-gate evaluation.
- PROD-009: model/provider changes are experiment-gated.
- PROD-010: provider/model/service tier are adaptive actions under versioned policy.
- RISK-0017: model/provider drift controlled by catalog refresh and re-eval.
- RISK-0019: versioned official pricing + observed usage, estimated vs billed separation.
- RISK-0022: capability/credential preflight and health/fallback states.
- RISK-0039: no cheap/fast route can bypass hard gates.
