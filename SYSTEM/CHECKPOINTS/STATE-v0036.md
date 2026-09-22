# CHECKPOINT — STATE v0036

`PROTOCOL_VERSION: 1.7.0`
`STATE_VERSION: 0036`
`BASE_MAIN_BEFORE_CANONICAL_INTEGRATION: 9f50b3d3ef1b3076f20a9c456a86177b8dcc8b84`
`WAVE: W004`
`STATUS: ACTIVE`

## Integrated in this checkpoint

### W004-T006-A01 — semantic ablation
- worker PR #141 merged to main before canonical fan-in;
- Actions run `35671065161` PASS;
- artifact `10669829767`, digest `sha256:b97cf40f836cf7672b6cf6cd95f17739912048353b595de095dbe7b00d3880f6`;
- 36/36 DEVELOPMENT outputs;
- hard-gate invariant 36/36; hard-fail compensation `0`;
- semantic-off automated-reference accuracy `0.083333`;
- semantic-on automated-reference accuracy `0.083333`;
- delta `+0.000000`;
- decision `NO_BACKEND_PREFERENCE`.

### W004-T007-A02 — bounded provider/model comparison
- A01 remains historical failed-cleanly provider-output truncation;
- worker PR #142 merged to main before canonical fan-in;
- accepted Actions run `35671546416` PASS;
- artifact `10671286471`, digest `sha256:ad6444365df0c188951a7ff68b7cd6351cc0eee83556386b3a9fd73940cc627f`;
- same four DEVELOPMENT sources / same prompt-config / 8 observed Groq calls;
- A03 not used as quality gold;
- 120B: preservation 3/4, quality 0.952083, numeric recall 0.958333, concept recall 1.000000, mean latency 1529.626 ms, derived cost 0.0016681500 USD;
- 20B: preservation 1/4, quality 0.856250, numeric recall 0.875000, concept recall 1.000000, mean latency 987.818 ms, derived cost 0.0009480750 USD;
- decision `NO_OVERALL_MODEL_PREFERENCE`.

## Evidence boundaries

- D-0017 remains LOCKED.
- `human_gold_eligible=false`.
- human agreement/preference/validation remain unobserved.
- audience thresholds remain `DIAGNOSTIC_ONLY`.
- semantic evidence does not justify a backend lock.
- provider/model evidence is a bounded source-preservation/latency/cost trade-off, not general superiority.

## DAG after integration

- T005: INTEGRATED.
- T006: INTEGRATED.
- T007: INTEGRATED via A02.
- T008-A01: READY; all declared dependencies satisfied.

## Next

Execute W004-T008-A01 clean-checkout release proof, then reconcile final risks, traceability, scorecards and stop conditions.
