# DR-5601 — Adaptive AI runtime routing policy

`TASK_ID: W005-T006`
`ATTEMPT_ID: A01`
`RESEARCH_DATE: 2026-09-22`
`STATUS: CANDIDATE_ARCHITECTURE; OPTIMIZER_PENDING_BENCHMARK`
`CONFIDENCE: HIGH on safety/observability architecture; MEDIUM on adaptive-policy form; LOW on any provider/model winner`

## Decision question

What runtime architecture should route provider/model/prompt/retrieval/repair/budget choices for Academy Suno while optimizing quality, factuality, latency, cost and reliability **without allowing any optimizer to compensate for or bypass source, factual, policy, schema, tenant-isolation or provenance hard gates**?

## Workload and constraints

Academy Suno is a stateful document → 3 audiences × 3 formats → eval → repair/review → aggregate workflow. Production requirements relevant here are PROD-005, PROD-007, PROD-009 and PROD-010. W004 provides a bounded Groq/GPT-OSS baseline, not a production winner. Production routing must be versioned, auditable, reversible, measurable, provider-neutral at the control-plane boundary and compatible with eval-driven CI/CD.

Critical constraints:

- hard gates are non-compensatory and live outside the optimizer;
- routing must preserve branch/source/tenant/provenance identity;
- retry/fallback cannot create unbounded cost/latency or silently weaken capability;
- provider/model catalogs, pricing, rate limits and model lifecycles drift;
- human-calibrated production audience thresholds are not yet available, so automated quality sensors remain bounded/diagnostic where applicable;
- no provider, model or gateway may become a production default without representative Academy workload evidence.

## Alternatives

| Alternative | Description | Strengths | Material limitations |
|---|---|---|---|
| A — Static baseline | Single fixed provider/model/prompt path, W004-style baseline | Simplest, easiest to reproduce | Does not satisfy the intended adaptive policy; poor resilience to price/model/capacity drift; no workload-aware optimization |
| B — Deterministic rules/cascade | Versioned eligibility + deterministic rules, bounded retries/fallbacks, optional cheap→strong cascade | Auditable, low operational risk, good initial champion | Rules can become brittle; may leave quality/cost/latency frontier gains unused |
| C — Managed/vendor routing | Provider/gateway-managed routing with explicit preferences/rules | Lower control-plane operational burden; existing products expose routing primitives | May be opaque, provider/platform-scoped, preview-limited or weak for Academy-specific hard gates; still requires post-route validation |
| D — Constrained adaptive router | Academy-owned policy interface; learned/contextual selection only among eligible candidates; shadow/canary exploration; same hard-gate envelope | Can adapt to workload and provider drift; compatible with multi-objective optimization and champion/challenger | Requires representative data, drift controls, unbiased feedback and stronger operational discipline |

## Evaluation criteria defined before decision

1. Critical hard-gate preservation — mandatory, non-compensatory.
2. Academy workload quality/factual preservation.
3. Latency distribution and deadline adherence.
4. Observed cost from token usage + versioned official price snapshot.
5. Reliability under rate limiting, capacity failures, timeouts and provider/model retirement.
6. Auditability/reproducibility of every route decision.
7. Safe exploration and rollback.
8. Provider/platform portability and lock-in.
9. Operational burden and failure surface.
10. Compatibility with eval-driven CI/CD and live evidence telemetry.

No single weighted score is used because hard-gate failures cannot be offset by savings elsewhere.

## Systematic source search

Search categories on 2026-09-22:

- current provider docs: model catalogs, pricing/service tiers, structured outputs, rate limits, deprecations and routing primitives;
- peer-reviewed / academic work on LLM cascades and quality-aware routing;
- production reliability guidance for timeout/retry/backoff/jitter;
- telemetry standards for GenAI provider/model/token attribution;
- managed routing/gateway patterns as counterfactuals.

Stopping rule: research stopped after four major provider families plus independent routing literature and reliability/telemetry standards converged on the same architectural trade-offs, and additional sources no longer introduced a materially new control-plane category. **Provider/model selection remains open because research saturation cannot substitute for the required representative benchmark.**

## Source table

| Source | Type/date | Claim supported | Limitation |
|---|---|---|---|
| OpenAI API pricing — https://developers.openai.com/pt-BR/api/docs/pricing | Primary vendor; current 2026-09-22 | multiple service tiers and materially different model prices; prices are mutable | vendor pricing is not workload quality evidence |
| OpenAI Flex — https://developers.openai.com/pt-BR/api/docs/guides/flex-processing | Primary vendor | lower-cost tier trades for longer responses / occasional unavailability | provider-specific/beta |
| OpenAI Fast mode — https://developers.openai.com/pt-BR/api/docs/guides/fast-mode | Primary vendor | latency tier can be a policy knob | provider-specific; vendor performance claim must be measured locally |
| Anthropic Sonnet 5 — https://www.anthropic.com/news/claude-sonnet-5 | Primary vendor, 2026 | current model/pricing snapshot demonstrates portfolio drift | launch material; not Academy benchmark |
| Anthropic model deprecations — https://docs.anthropic.com/en/docs/about-claude/model-deprecations | Primary vendor | active/deprecated/retired lifecycle requires catalog health/versioning | Anthropic-specific |
| Google Vertex `RoutingConfig` — https://docs.cloud.google.com/vertex-ai/generative-ai/docs/reference/rpc/google.cloud.aiplatform.v1 | Primary vendor | managed auto-routing supports quality/balanced/cost preferences | platform-specific; opaque router quality on Academy workload unknown |
| Google API Gateway model routing — https://docs.cloud.google.com/api-gateway/docs/model-routing-overview | Primary vendor, Public Preview | managed multi-family traffic layer exists; current preview routes by model tag/name | preview and host/platform constraints; not a learned Academy router |
| Groq supported models — https://console.groq.com/docs/models | Primary vendor | W004 GPT-OSS 20B/120B remain valid benchmark seeds; current price/speed catalog is mutable | vendor speed is not Academy end-to-end latency |
| Groq Flex — https://console.groq.com/docs/flex-processing | Primary vendor | capacity tier can fail fast with 498 and explicitly recommends jittered retry | Groq-specific |
| Groq rate limits — https://console.groq.com/docs/rate-limits | Primary vendor | 429 + retry/rate headers support bounded retry policy | account limits vary |
| Hybrid LLM, ICLR 2024 — https://proceedings.iclr.cc/paper_files/paper/2024/hash/b47d93c99fa22ac0b377578af0a1f63a-Abstract-Conference.html | Peer-reviewed research | quality-aware query routing can reduce expensive-model calls on evaluated tasks | external tasks; effect size cannot be transferred to Academy |
| FrugalGPT — https://arxiv.org/abs/2305.05176 | Research | cascades/prompt adaptation/model approximation are viable cost-quality strategies | older external benchmark; not Academy evidence |
| AWS Builders’ Library retries/backoff/jitter — https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/ | Primary operational guidance | retries need timeout, bounded backoff and jitter to avoid correlated overload | general distributed-systems guidance, not LLM-specific |
| OpenTelemetry GenAI attributes — https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/ | Open standard | provider/model/token/workflow telemetry has standard semantic conventions; prompt/output fields may be sensitive | conventions evolve; content capture must be redacted/opt-in |

## Findings

### 1. Put a deterministic safety envelope outside the optimizer

The runtime SHOULD be two-layered:

1. **Eligibility + hard-gate layer**: tenant/source/provenance binding, allowed capabilities, policy constraints, schema contract and provider/model health. A candidate failing eligibility never reaches the optimizer.
2. **Optimization layer**: only among eligible routes, select provider/model + prompt variant + retrieval profile + repair policy + budget/service tier.
3. **Post-route acceptance layer**: every produced output passes the same factual/source/policy/schema/provenance checks before promotion. Fallbacks and repairs do not bypass this layer.

This separation directly controls RISK-0039: cost/latency cannot compensate for critical quality/safety failure.

### 2. Do not invent a universal scalar utility

Use lexicographic constraints / Pareto analysis rather than a fabricated aggregate score:

- first: all critical hard requirements PASS;
- second: meet evidence-backed quality/reliability floors once established;
- third: compare cost, p50/p95/p99 latency, reliability and bounded quality on the Pareto frontier.

A mathematical optimizer MAY later use constrained expected utility, but weights/penalties are `PENDING_EVIDENCE` until Academy experiments establish them.

### 3. Exploration must be staged

Recommended promotion sequence:

- **offline champion/challenger** on versioned DEV/CALIBRATION/HELD-OUT slices;
- **shadow routing** to log counterfactual choices without affecting recipients;
- **bounded canary exploration** only among already eligible routes, with fixed experiment budget, stable assignment and automatic stop-loss;
- **exploitation** by the current champion with periodic re-challenge.

Online learning MUST NOT auto-promote a policy directly from self-judge reward. Human-calibrated evidence, once available, should be incorporated without relabeling current automated sensors as human gold.

### 4. Retry/fallback owns a single end-to-end budget

Error taxonomy:

- invalid request/auth/tenant/policy/schema incompatibility: fail closed; no blind retry;
- 429 / transient 5xx / explicit capacity failures: bounded retry, honor `Retry-After` where present, exponential backoff + jitter;
- timeout: cancel on per-attempt deadline and consider fallback only if the remaining end-to-end deadline permits;
- provider/model unhealthy or retired: circuit-open / catalog-disabled route; choose an equivalent eligible candidate.

Only one layer should own retries to prevent multiplicative retry storms. Repairs are targeted, capped and freshly evaluated.

### 5. Policy is an immutable, reversible artifact

Every policy version should carry:

- policy semantic version + content hash;
- candidate-catalog snapshot/version;
- prompt/retrieval/eval/repair configuration versions;
- pricing snapshot reference and timestamp;
- experiment ID / rationale;
- rollout mode (`offline`, `shadow`, `canary`, `active`);
- previous known-good version and explicit rollback pointer.

Rollout should be atomic, assignments sticky at run/tenant-safe key scope, and rollback should require no data migration.

### 6. Telemetry is part of correctness

Minimum route event/span fields:

- `route_decision_id`, run/branch identifiers, pseudonymous tenant/workspace correlation;
- policy version/hash, candidate catalog version;
- candidates considered + rejection reason;
- chosen provider/model/service tier + prompt/retrieval/repair/budget versions;
- exploration/shadow flag;
- queue/provider/TTFT/end-to-end timings where available;
- request/response/cache token counts and provider request ID;
- observed retries, fallback chain, circuit state, error taxonomy;
- versioned estimated cost and, when available, billed cost kept distinct;
- all hard-gate results, repair rounds and final acceptance state.

OpenTelemetry GenAI attributes are a suitable base vocabulary. Full prompts/documents/outputs are **not** default telemetry because the standard itself warns these fields can contain sensitive/PII data.

## Decision

**Architecture pattern: CANDIDATE FOR T010 INTEGRATION.**

Adopt a provider-neutral, versioned routing-policy interface with a deterministic eligibility/hard-gate envelope, bounded retry/fallback semantics, complete route telemetry, staged shadow/canary rollout and atomic rollback. Begin production implementation with a deterministic rules/cascade champion because it is auditable; keep a learned/contextual router as a plug-compatible challenger that cannot be promoted until the representative benchmark demonstrates a non-dominated improvement.

**Exact optimizer algorithm: `PENDING_BENCHMARK`.**

**Gateway/control-plane product (custom thin layer vs LiteLLM/managed gateway/etc.): `PENDING_T010/T013`; this task does not preempt developer-platform/toolchain synthesis.**

## Reversal conditions

Reopen the architecture decision if:

- a managed router demonstrates Academy hard-gate transparency + materially lower operational burden without unacceptable lock-in;
- representative data shows deterministic routing is already Pareto-optimal and learned routing adds no material gain;
- a provider/API constraint makes the provider-neutral policy boundary impractical;
- T004/T007 security/observability research imposes stricter data/telemetry constraints;
- T009 benchmark methodology changes the experimental validity requirements.

## Traceability

- PROD-005: provider abstraction + observed route identity.
- PROD-007: post-route hybrid eval remains mandatory.
- PROD-009: policy/model/prompt changes require regression/experiment before promotion.
- PROD-010: adaptive dimensions are versioned, auditable, reversible and cannot relax hard gates.
- RISK-0005: capped repair/retry and end-to-end attempt budget.
- RISK-0017: candidate catalog lifecycle + periodic re-evaluation.
- RISK-0019: usage-based cost with versioned official price snapshot; estimated vs billed separated.
- RISK-0022: provider health/circuit/fallback and capability preflight.
- RISK-0039: hard gates outside optimizer + post-route revalidation.
