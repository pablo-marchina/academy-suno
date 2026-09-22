# DR — W005-T005 evaluation framework/tooling

`DR_ID: W005-T005-DR02`  
`STATUS: PENDING_EVIDENCE`  
`DATE: 2026-09-22`  
`SCOPE: offline eval harness, CI regression, experiment artifacts, online evaluation`

## Decision question

Should Academy Suno replace or wrap its current native Python/pytest evaluation harness with an external evaluation framework for production?

## Non-negotiable criteria

Any candidate must preserve:

1. deterministic non-compensatory hard gates;
2. versioned dataset/config provenance and locally inspectable artifacts;
3. baseline-vs-candidate evaluation on the same frozen items;
4. custom PT-BR audience/factual/numeric/entity/date/concept metrics;
5. human-calibration data without calling model labels human gold;
6. CI execution with explicit pass/block semantics;
7. provider/model neutrality where practical;
8. privacy-safe operation for source documents;
9. exportable raw results sufficient to reproduce a decision;
10. no inherited default threshold becoming a project threshold without evidence.

## Candidates

### A — Native typed Python harness + pytest (current baseline)

**Strengths:** maximum control over hard-gate semantics, existing code fit, local reproducibility, minimal new dependency/lock-in.  
**Weaknesses:** more internal work for dataset UI, comparative experiment views, human queues, online evaluation and red-team ergonomics.  
**Status:** baseline to beat; not an exclusive production lock.

### B — Promptfoo

Current documentation shows local/open-source execution, provider comparisons, deterministic/custom assertions, model-graded assertions, CI integration, browser reports and red-team workflows. This maps well to provider bakeoffs and security/adversarial evals.

Sources:
- assertions/metrics: https://www.promptfoo.dev/docs/configuration/expected-outputs/
- CI/CD: https://www.promptfoo.dev/docs/integrations/ci-cd/
- red teaming: https://www.promptfoo.dev/docs/guides/llm-redteaming/

**Risk:** YAML/assertion defaults and model-graded thresholds must not replace Academy Suno's evidence/threshold policy; Node runtime introduces an additional toolchain.

### C — DeepEval

Current documentation supports local datasets, end-to-end/component evaluation, custom/built-in metrics and CI-oriented test execution. It is Python-native and therefore comparatively close to the current stack.

Sources:
- evaluation overview: https://deepeval.com/docs/evaluation-introduction
- datasets: https://deepeval.com/docs/evaluation-datasets
- CI/CD: https://deepeval.com/docs/evaluation-unit-testing-in-ci-cd

**Risk:** many built-in metrics are LLM-as-a-judge and documented metric defaults include generic pass thresholds. Those defaults are not admissible as Suno production thresholds without independent calibration.

### D — LangSmith evaluation

Current documentation supports offline benchmarking/regression, code and LLM evaluators, pairwise evaluation, online evaluators, datasets/experiments and human-feedback workflows. It is framework-agnostic from the application side.

Sources:
- evaluation types: https://docs.langchain.com/langsmith/evaluation-types
- product evaluation/human feedback: https://www.langchain.com/langsmith/evaluation

**Risk:** cloud/platform dependency and data-governance implications require an explicit privacy/operational review; production artifacts must remain exportable and decision provenance must not depend only on a hosted UI.

## Evidence matrix

| Criterion | Native | Promptfoo | DeepEval | LangSmith |
|---|---|---|---|---|
| deterministic custom hard gates | strong/current | supported | supported/custom | supported/code evaluators |
| Python fit | strong | weaker (Node-centric) | strong | strong SDK |
| local-first artifact path | strong | strong | supported | mixed/hosted-centric |
| model-judge support | custom | supported | extensive | supported |
| CI workflow | current pytest | documented | documented | SDK/workflow dependent |
| online evaluation | custom work | limited relative to hosted observability | platform-dependent extension | documented |
| human review workflow | custom work | not primary strength | platform-dependent | documented |
| red-team ergonomics | custom | strong | available ecosystem capabilities, benchmark needed | not primary evidence here |
| project threshold safety | full control | must override defaults | must override defaults | must define own rules |

This table is capability research, not a performance benchmark.

## Representative bakeoff required

Before `LOCK`, run the same versioned workload through the native baseline and at least the strongest external candidates:

1. one deterministic critical factual/numeric fixture set;
2. one structured audience/jargon/readability suite;
3. one calibrated LLM-judge rubric with raw rationale/artifact export;
4. one paired baseline-vs-candidate experiment using the production metadata schema;
5. CI execution that intentionally introduces a critical hard-gate regression and proves it blocks;
6. export/replay from clean checkout without relying on a private UI;
7. measure setup/runtime overhead, artifact completeness, integration LOC, execution time, provider cost, failure diagnosability and privacy/data-egress behavior.

## Decision

`PENDING_EVIDENCE`.

Do **not** rewrite the current harness or lock an external framework from feature lists alone. Keep the native typed harness as the authoritative baseline and adapter boundary. An external tool may be added for capabilities that win the representative bakeoff while the project's dataset/experiment schemas and hard-gate semantics remain canonical.

## Reversal / lock condition

Promote a candidate to `LOCK` only after the representative bakeoff demonstrates a material advantage with no loss of provenance, hard-gate control, reproducibility or privacy requirements. If no candidate materially beats the native baseline, record `NO_PREFERENCE`/retain-native rather than adopting a framework for fashion.
