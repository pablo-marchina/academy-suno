# TASK LEDGER

Somente Orchestrator com lease ativo altera este arquivo.

## Status
`PLANNED | READY | RUNNING | BLOCKED | RESULT_RECEIVED | INTEGRATED | CANCELLED | STALE`

| Task ID | Attempt | Base State | Base Commit | Role | Status | Dependencies | Issue / PR | Integrated State |
|---|---|---:|---|---|---|---|---|---|
| BOOT-T001 | A01 | 0001 | legacy | Orchestrator | INTEGRATED | none | PR #1 | 0002 |
| BOOT-T002 | A01 | 0007 | 434123de90e2cebb8d60bb4020a90c09ec48bcab | Orchestrator | INTEGRATED | BOOT-T001 | Issue #2 | 0008 |
| W001-T001 | A01 | 0008 | 3f437ab4f21b88ea4b7fe0771ca0f7c82ed51235 | Researcher | INTEGRATED | none | Issue #10 | 0009 |
| W001-T002 | A01 | 0008 | 3f437ab4f21b88ea4b7fe0771ca0f7c82ed51235 | Analyst | INTEGRATED | none | Issue #11 | 0009 |
| W001-T003 | A01 | 0008 | 3f437ab4f21b88ea4b7fe0771ca0f7c82ed51235 | Analyst | INTEGRATED | none | Issue #12 | 0009 |
| W001-T004 | A01 | 0008 | 3f437ab4f21b88ea4b7fe0771ca0f7c82ed51235 | Analyst | INTEGRATED | none | Issue #13 | 0009 |
| W001-T005 | A01 | 0008 | 3f437ab4f21b88ea4b7fe0771ca0f7c82ed51235 | Analyst | INTEGRATED | none | Issue #14 | 0009 |
| W001-T006 | A01 | 0008 | 3f437ab4f21b88ea4b7fe0771ca0f7c82ed51235 | Analyst | INTEGRATED | none | Issue #15 | 0009 |
| W001-T007 | A01 | 0008 | 3f437ab4f21b88ea4b7fe0771ca0f7c82ed51235 | Builder/Writer | INTEGRATED | none | Issue #16 | 0009 |
| W001-T008 | A01 | 0008 | 3f437ab4f21b88ea4b7fe0771ca0f7c82ed51235 | Critic/Researcher | INTEGRATED | none | Issue #17 | 0009 |
| W001-T009 | A01 | 0010 | 762598b64216ce4ec272a50dd49ecbea08e8ae59 | Synthesizer | INTEGRATED | W001-T002,W001-T003,W001-T004,W001-T005 | Issue #18 | 0011 |
| W001-T010 | A01 | 0011 | d6d7519f0e119d58509cbabdb5f636cac0698ff0 | Synthesizer | INTEGRATED | W001-T001,W001-T006,W001-T007,W001-T008,W001-T009 | Issue #19 | 0012 |
| W002-T001 | A01 | 0013 | f9ac1a08d717d41b7a424bbc3a5a392af5f77e0d | Builder | INTEGRATED | none | Issue #33 | 0014 |
| W002-T002 | A01 | 0013 | f9ac1a08d717d41b7a424bbc3a5a392af5f77e0d | Builder/Analyst | INTEGRATED | none | Issue #34 | 0014 |
| W002-T003 | A01 | 0013 | f9ac1a08d717d41b7a424bbc3a5a392af5f77e0d | Builder/Critic | INTEGRATED | none | Issue #35 | 0014 |
| W002-T004 | A01 | 0013 | f9ac1a08d717d41b7a424bbc3a5a392af5f77e0d | Builder | INTEGRATED | none | Issue #36 | 0014 |
| W002-T005 | A01 | 0013 | f9ac1a08d717d41b7a424bbc3a5a392af5f77e0d | Builder/Analyst | INTEGRATED | none | Issue #37 | 0014 |
| W002-T006 | A01 | 0013 | f9ac1a08d717d41b7a424bbc3a5a392af5f77e0d | Critic/Builder | INTEGRATED | none | Issue #38 | 0014 |
| W002-T007 | A01 | 0014 | 988beae91aad40acbcdd3189bdf8f0d2e216c832 | Builder | INTEGRATED | W002-T001,W002-T002,W002-T006 | Issue #39 / PR #56 | 0015 |
| W002-T008 | A01 | 0014 | 988beae91aad40acbcdd3189bdf8f0d2e216c832 | Builder | INTEGRATED | W002-T001,W002-T003 | Issue #40 / PR #54 | 0015 |
| W002-T009 | A01 | 0014 | 988beae91aad40acbcdd3189bdf8f0d2e216c832 | Builder | INTEGRATED | W002-T001,W002-T004 | Issue #41 / PR #55 | 0015 |
| W002-T010 | A01 | 0015 | da66fc64ccb0b7780684059a2a3fd33afe11c904 | Synthesizer/Builder | INTEGRATED | W002-T005,W002-T007,W002-T008,W002-T009 | Issue #42 / PR #58 | 0016 |
| W003-T001 | A01 | 0016 | bd29959b081d8f70a40b420ab715f66ac5e59154 | Analyst/Evaluator | INTEGRATED | none | Issue #59 / PR #73 | 0017 |
| W003-T002 | A01 | 0016 | bd29959b081d8f70a40b420ab715f66ac5e59154 | Builder/Evaluator | INTEGRATED | none | Issue #60 / PR #70 | 0017 |
| W003-T003 | A01 | 0016 | bd29959b081d8f70a40b420ab715f66ac5e59154 | Builder/Architect | INTEGRATED | none | Issue #61 / PR #72 | 0017 |
| W003-T004 | A01 | 0016 | bd29959b081d8f70a40b420ab715f66ac5e59154 | Analyst/Builder | INTEGRATED | none | Issue #62 / PR #71 | 0017 |
| W003-T005 | A01 | 0016 | bd29959b081d8f70a40b420ab715f66ac5e59154 | Auditor/Builder | INTEGRATED | none | Issue #63 / PR #69 | 0017 |
| W003-T006 | A01 | 0017 | fcfd960edef139062c95b7c37563982986d9783d | Builder/Evaluator | INTEGRATED | W003-T002,W003-T003,W003-T004 | Issue #64 / PR #75 | 0018 |
| W003-T007 | A01 | 0017 | fcfd960edef139062c95b7c37563982986d9783d | Builder/Analyst | INTEGRATED | W003-T003 | Issue #65 / PR #76 | 0018 |
| W003-T008 | A01 | 0018 | 1a8999c954ab86000e2ae7608616ab5828fbcdfe | Evaluator/Analyst | INTEGRATED | W003-T001,W003-T002,W003-T004,W003-T007 | Issue #66 / PR #78 | 0019 |
| W003-T009 | A01 | 0019 | 8e84982a8ecd492a925d25ae1e37bedcfe0f889c | Synthesizer/Auditor | INTEGRATED | W003-T005,W003-T006,W003-T007,W003-T008 | Issue #67 / PR #80 | 0020 |
| W004-T001 | A01 | 0020 | 2555308805c2b3eac4ef494605c35e01697f8884 | Builder/UX | INTEGRATED | none | Issue #81 / PR #93 | 0021 |
| W004-T002 | A01 | 0020 | 2555308805c2b3eac4ef494605c35e01697f8884 | Analyst/Evaluator | INTEGRATED | none | Issue #82 / PR #94 | 0021 |
| W004-T003 | A01 | 0020 | 2555308805c2b3eac4ef494605c35e01697f8884 | Builder/Analyst | INTEGRATED | none | Issue #83 / PR #91 | 0021 |
| W004-T004 | A01 | 0020 | 2555308805c2b3eac4ef494605c35e01697f8884 | Builder/Analyst | BLOCKED | none | Issue #84 / PR #90 | — |
| W004-T005 | A01 | 0021 | 53921e41e966c04a2644542ab9619baa6a66170b | Evaluator/Analyst | BLOCKED | W004-T002 | Issue #85 | — |
| W004-T006 | A01 | release-after-deps | release-after-deps | Evaluator/Builder | PLANNED | W004-T005 | Issue #86 | — |
| W004-T007 | A01 | release-after-deps | release-after-deps | Analyst/Evaluator | PLANNED | W004-T004,W004-T005 | Issue #87 | — |
| W004-T008 | A01 | release-after-deps | release-after-deps | Synthesizer/Auditor | PLANNED | W004-T001,W004-T003,W004-T005,W004-T006,W004-T007 | Issue #88 | — |
| W004-T009 | A01 | 0022 | 7059381fd34aee20f159a477ba61eb4c4048af45 | Builder/UX | INTEGRATED | W004-T002 | Issue #95 / PR #100 | 0023 |
| W004-T010 | A01 | 0022 | 7059381fd34aee20f159a477ba61eb4c4048af45 | Builder/Analyst | INTEGRATED | none | Issue #96 / PR #101 | 0023 |
| W004-T011 | A01 | 0022 | 7059381fd34aee20f159a477ba61eb4c4048af45 | Writer/Auditor/Builder | INTEGRATED | W004-T001,W004-T003 | Issue #97 / PR #99 | 0023 |
| W004-T012 | A01 | 0023 | 2fcf016ade631e9307ec0d222d633c066adf4c88 | Auditor/Builder | INTEGRATED | W004-T011 | Issue #102 / PR #105 | 0024 |
| W004-T013 | A01 | 0023 | 2fcf016ade631e9307ec0d222d633c066adf4c88 | Critic/Auditor | INTEGRATED | W004-T001,W004-T003,W004-T009,W004-T011 | Issue #103 / PR #106 | 0024 |
| W004-T014 | A01 | 0024 | 83a5ffc1eacdd245773845eeae9d4542aa683c4f | Builder/UX/Data | INTEGRATED | W004-T001,W004-T003,W004-T012,W004-T013 | Issue #107 / PR #112 | 0025 |
| W004-T015 | A01 | 0024 | 83a5ffc1eacdd245773845eeae9d4542aa683c4f | Writer/Analyst/Auditor | INTEGRATED | W004-T002,W004-T010,W004-T011,W004-T012,W004-T013 | Issue #108 / PR #111 | 0025 |
| W004-T016 | A01 | 0025 | 0980534866ed84c2f6af28453f6cb20cd1c7efba | Demo/Builder/Auditor | BLOCKED | W004-T012,W004-T014,W004-T015 | Issue #109 / PR #114 | — |
| W004-T017 | A01 | 0026 | 6269c4b8466ff794d1f448507f2e4e3ed15d48dd | Demo/Builder/Auditor | INTEGRATED | W004-T012,W004-T014,W004-T015 | Issue #115 / PR #117 | 0027 |
| W004-T018 | A01 | 0027 | abd1c5c470719a68545023bbbf65cab46e708dd5 | Critic/Auditor | INTEGRATED | W004-T013,W004-T014,W004-T015,W004-T017 | Issue #118 / PR #120 | 0028 |
| W004-T019 | A01 | 0028 | 584a23406291a42c29eb795d34bedd2de0357647 | Demo/Builder/Writer/Auditor | INTEGRATED | W004-T014,W004-T015,W004-T017,W004-T018 | Issue #121 / PR #124 | 0029 |
| W004-T020 | A01 | 0029 | ea6dbcdab3ca7b61117824b0527e45252370bae9 | Critic/Auditor | INTEGRATED | W004-T019 | Issue #122 / PR #126 | 0030 |
| W004-T021 | A01 | 0030 | bind-after-merge | Release/Artifact Auditor | READY | W004-T019,W004-T020 | Issue #127 | — |

## W003 outcome

W003 COMPLETE: mechanics proof source→9 jobs→eval→targeted repair→aggregate; persistent RunStore reopen/resume; separate transport retry vs quality repair; hard-gate non-compensation; telemetry lineage. Calibration remains DIAGNOSTIC_ONLY and production provider/parser/semantic quality remains unclaimed.

## W004 evidence through STATE 0030

- T001–T003: cockpit, representative corpus/human-calibration preparation and role-aware parser/source-trust behavior integrated.
- T004 A01 remains BLOCKED for real credentialed provider execution.
- T005 A01 remains BLOCKED for two genuinely independent human primary annotation streams; no pseudo-human/model gold allowed.
- T009/T010: human annotation operator and manual secret-safe provider path integrated without satisfying external blockers by themselves.
- T011/T012: release packet + clean task-specific release smoke integrated; 9/9 mechanics and persisted FAIL→repair→PASS observed.
- T013: first blind review `NOT_PASS`; T014/T015 remediated recipient app/report gaps.
- T017: real Playwright/Chromium recording succeeded with real BCB PDF, exact hashes/artifacts and duration `7.200s <= 300s`.
- T018 directly inspected T017 and kept `BLIND_REVIEW: NOT_PASS` because the 7.2s silent clip was not evaluator-usable.
- T019 is INTEGRATED: accepted Actions run `35636285651`; paced real-browser MP4 `69.12s <= 300s`, SHA-256 `c3451658df0a05e69f6d883a9861629a0fe8bef396288b9861d8010e850907e5`; success `SOURCE_READY/PASS` path first with 9/9 + repair lineage, BCB fail-closed safety negative-control second; nine decoded post-encode frame validations PASS; README/submission packet refreshed.
- T020 is INTEGRATED: independent direct artifact review `VIDEO_PACKAGE_REVIEW: PASS`, zero new CRITICAL/HIGH internal findings; F-001/F-002/F-003/F-007/F-008 pass in review scope. Overall project/release readiness remains pending external human/provider gates.
- T021 is READY after exact post-merge bind to preserve the accepted T019 MP4 in durable submission-controlled storage and eliminate the remaining Actions-retention risk without regenerating the binary.

## Rules

Toda task deve apontar para hard gate, Success dimension, requisito/pain, assumption/risk ou dependency crítica. Reexecução cria novo attempt. RESULT_RECEIVED não significa integrado. Wave manifest é fonte do DAG. Para protocolo 1.6.0+, runtime status é reconstruído por `SYSTEM/TASK_SIGNALS.md` antes de qualquer atualização canônica.

## Next

Bind W004-T021 to exact STATE 0030 post-merge SHA and execute it. Keep T004/T005 external blockers explicit; T006/T007/T008 remain dependency-blocked by valid human/provider evidence. Do not infer overall release readiness from the video/package PASS.
