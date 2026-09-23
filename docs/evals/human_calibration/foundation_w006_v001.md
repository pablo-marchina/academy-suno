# W006 human-calibration foundation v001

`TASK_ID: W006-T010`  
`ATTEMPT_ID: A01`  
`FOUNDATION_VERSION: w006-human-calibration-foundation-v001`  
`EVIDENCE_STATUS: HUMAN_COLLECTION_NOT_OBSERVED`  
`AUDIENCE_THRESHOLD_STATUS: DIAGNOSTIC_ONLY`

## 1. Scope and authority

This artifact operationalizes the accepted W005 production evaluation protocol for W006. It consumes:

- the W006-T001 versioned identity/provenance/evaluator contract boundary;
- the W006-T004 source-group/provenance boundary and its explicit `NO_PRODUCTION_PARSER_WINNER`;
- the W005 rule that strong audience claims require independent human calibration plus frozen HELD_OUT replication.

It does not promote parser, model, provider, judge, threshold, or framework winners.

## 2. Versioned partitions and sample accounting

`data/evals/production/w006/partition_manifest_v001.json` is the bootstrap partition manifest. The split unit is `source_group_id`, never a generated branch.

All 3 audiences × 3 formats from one source share the same source-group identity. Digital/scanned/encrypted/malformed parser variants from T004 also stay inside their parent source group. Therefore nine derived 3×3 siblings have independent source `N=1`, not `N=9`.

The two historical W004 HELD_OUT source groups remain HELD_OUT. The four historical W004 development groups are assigned between DEV and CALIBRATION only to make the protocol executable. This six-source bootstrap is not asserted to represent production traffic and cannot by itself justify a production threshold. Corpus expansion must follow census + risk coverage + precision/power planning.

If a HELD_OUT item is inspected in a way that changes prompts, rubric, evaluator logic, judge config, thresholds, model choice, or repair policy, the release set is contaminated: rotate/version the split before any release claim.

## 3. Blind independent human collection

Each scored CALIBRATION or future HELD_OUT item receives two independent primary records:

- `PRIMARY_A`
- `PRIMARY_B`

A primary annotator may see only the frozen source evidence needed for the rubric and the frozen candidate output. The packet must hide generation target audience, evaluator/judge outputs, generator/provider/model/prompt identity, baseline/candidate arm identity, peer annotation, and HELD_OUT tuning analysis.

The same person must not fill both primary streams for the same item. Annotator identity is pseudonymous but stable enough to prove stream independence. Training/qualification examples are separate from scored packets.

Records conform to `data/evals/production/w006/human_annotation_record_schema_v001.json`.

## 4. Agreement before adjudication

Freeze both primary streams before computing agreement. Preserve pre-adjudication evidence permanently.

Required report, by overall and declared slices with sample counts:

- paired item count and missingness;
- raw agreement;
- `PRIMARY_A → PRIMARY_B` confusion matrix;
- `UNSCORABLE` rates;
- Cohen kappa where defined;
- quadratic weighted kappa on ordered scorable labels where defined;
- disagreement on every non-compensatory check;
- source-group-aware uncertainty/bootstrapping when sample size makes it meaningful.

Agreement is evidence about annotation consistency, not proof of construct validity. Low agreement is never hidden by adjudication.

## 5. Adjudication

Adjudication is triggered when:

- primary audience labels differ;
- either primary is `UNSCORABLE`;
- a non-compensatory check differs;
- either primary marks a hard check `FAIL` or `REVIEW_REQUIRED`;
- a predeclared high-risk slice requires third review.

The adjudicator must be distinct from both primaries for the item, sees the frozen primary records only after both are complete, and remains blind to target/evaluator/judge/arm identity. The adjudication record references both primary annotation IDs and gives a rationale.

If evidence remains insufficient, use `UNRESOLVED`; never force a gold label.

## 6. Human evidence classes

Only independent human work may populate:

- `HUMAN_INDEPENDENT_CALIBRATION`
- `HUMAN_ADJUDICATED_GOLD`

Model-generated labels, W004 automated calibration, deterministic metrics, synthetic fixtures, or model-judge outputs cannot be re-labeled as human gold. The validator explicitly rejects that path.

Actual human annotation is an external evidence dependency for this attempt. Current observed human primary records: `0`. Current adjudicated human-gold items: `0`.

## 7. Secondary judge calibration

`data/evals/production/w006/judge_calibration_contract_v001.json` is the release gate for any LLM/model judge.

A judge may be promoted to `MODEL_JUDGE_CALIBRATED` only after:

1. comparison against independent human reference on CALIBRATION;
2. confusion/error reporting by audience, format, and source-risk slice;
3. order/position swap testing for pairwise tasks;
4. repeated-run stability testing when nondeterministic;
5. freezing provider/model/prompt/config;
6. separate HELD_OUT replication after freeze.

Judge outputs remain secondary and can never override factual/source/policy hard gates.

Because no independent human reference is observed in this attempt, judge release calibration is `BLOCKED_PENDING_HUMAN_REFERENCE`.

## 8. Paired baseline/candidate experiment contract

`data/evals/production/w006/paired_experiment_contract_v001.json` requires:

- same dataset version and exact source/branch membership for both arms;
- pairing key `source_group_id × audience × format`;
- uncertainty clustered by source group;
- raw baseline and candidate outputs persisted;
- versioned evaluator/config identities persisted;
- critical hard-gate regression tolerance exactly `0`;
- no scalar utility that compensates hard-gate failure;
- no HELD_OUT tuning after results are viewed.

Soft non-inferiority/superiority margins remain `PENDING_EVIDENCE` until justified from pilot/human/business tolerance. Audience thresholds remain `DIAGNOSTIC_ONLY`.

## 9. Promotion sequence

A strong production audience-threshold claim requires this order:

1. expand/version corpus from production/source census and risk coverage;
2. freeze CALIBRATION packets and collect independent primaries;
3. compute agreement before adjudication;
4. adjudicate triggered cases without target/evaluator leakage;
5. calibrate candidate audience/judge rule on CALIBRATION only;
6. freeze evaluator/judge/threshold rule;
7. run separately frozen HELD_OUT replication;
8. report confusion matrix, source-group sample counts, uncertainty and critical failures;
9. promote only if the predeclared operating claim is supported.

Until step 7 is completed with sufficient evidence, production threshold freeze is forbidden.

## 10. Hard gates

The following are non-compensatory:

- factual/source/policy failure;
- numeric/entity/date material error;
- material concept loss/contradiction;
- critical schema/branch/format failure;
- split/leakage/provenance failure.

Quality, latency, cost, readability, judge score, or aggregate utility cannot erase a hard-gate failure.

## 11. Reopen conditions

Version this foundation when source distribution changes materially, the rubric proves ambiguous on a material slice, source identity/provenance changes, judge/provider/config changes, new hard-failure categories are discovered, or the six-source bootstrap is replaced by the evidence-derived production corpus.
