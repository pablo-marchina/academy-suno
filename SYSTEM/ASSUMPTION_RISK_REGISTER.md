# ASSUMPTION & RISK REGISTER

## Assumptions

| ID | Assumption | Evidence | Impact if wrong | Uncertainty | Validation / mitigation | Owner | Status |
|---|---|---|---|---|---|---|---|
| A-0001 | Para o vídeo final, usar <=5:00 como regra operacional segura | E-0001,T019,T020,T021,T008-A02 | CRITICAL | LOW | final W004 MP4 69.120s; future final video also <=5:00 | Orchestrator | CONTROLLED |
| A-0002 | Usuário interno provável é conteúdo/editorial/research; owner real não identificado | E-0002 + inferência | HIGH | HIGH | não afirmar workflow interno; manter adapters modulares | Research | OPEN_EXTERNAL |
| A-0003 | Valor principal é `content transformation + trust layer`, não simples resumo | W001–W004; T020; T008-A02 | HIGH | MEDIUM | produto/evidence layer executados; ROI real não alegado | Strategy | SUPPORTED_HYPOTHESIS |
| A-0004 | Níveis de sofisticação exigem calibração além de prompts | T005-A02; D-0017 | HIGH | MEDIUM | automated blind calibration aceita para W004; production thresholds require stronger evidence | Eval | CONTROLLED_CASE_WAIVER_PRODUCTION_OPEN |
| A-0005 | Pydantic nas fronteiras + orchestration evidence-driven são adequados | W002,W003,T008-A02 | MEDIUM | LOW | clean E2E mechanics observados; production runtime ainda deve passar DRG | Architecture | SUPPORTED_BASELINE |
| A-0006 | Não há dataset gold/anotado fornecido pelo parceiro | briefing; T005-A02; D-0017 | HIGH | HIGH | W004 waiver; production calibration protocol deve criar/obter evidence stronger | Eval | OPEN_PRODUCTION_HUMAN_EVIDENCE |
| A-0007 | Imitação de voz Suno pode ser desejável, mas não é requisito hard do briefing | E-0001,E-0002 | MEDIUM | HIGH | manter opcional; não alegar style-transfer validado | Content | OPEN_NONCRITICAL |
| A-0008 | Documentos públicos-alvo podem ser parseados com fail-closed suficiente para demo/case | T014,T019,T020,T008-A02 | HIGH | LOW-MEDIUM | positive path + BCB ambiguity negative-control observados; production corpus broadened later | Data | SUPPORTED_CASE_SCOPE |
| A-0009 | Flesch PT-BR precisa implementação/teste controlado | W003,T005-A02 | MEDIUM | LOW | versioned implementation + diagnostics; no threshold freeze | Eval | SUPPORTED_IMPLEMENTED |
| A-0010 | Semantic/LLM judge deve ser sensor secundário, não árbitro único | W003,T006-A01 | HIGH | LOW | hard-gate non-compensation; zero measured gain → no backend lock | Eval | CONTROLLED_BY_DESIGN |
| A-0011 | Valor operacional real pode incluir tempo/retrabalho/reuso multicanal | inferência + telemetry/provider evidence | HIGH | HIGH | não emitir ROI claim sem baseline/owner/workflow Suno | Partner Research | OPEN_EXTERNAL_VALUE_MAGNITUDE |
| A-0012 | Concurrency/capacity target real ainda não é conhecido | E-0025/operator scope says multiple users, no target count | HIGH | HIGH | run saturation curve; define SLO/capacity from evidence, not arbitrary number | SRE | OPEN_W005_RESEARCH |
| A-0013 | Deployment/provider/cloud target específico não foi imposto | E-0025 | HIGH | HIGH | compare deploy/runtime alternatives under DRG; keep portable interfaces | Architecture/SRE | OPEN_W005_RESEARCH |
| A-0014 | Nenhuma stack candidata é winner de produção ainda | D-0016,D-0018 | CRITICAL | LOW | current components are baselines; W005 DRG/bakeoffs before lock | Orchestrator | CONTROLLED_NO_PREMATURE_LOCK |
| A-0015 | “Sem demo” significa sem sistema fake/descartável; vídeo obrigatório continua | E-0001 + D-0018 | CRITICAL | LOW | single real product path + final <=5m video | Orchestrator | CONTROLLED |
| A-0016 | Maior visualização frontend é desejada, mas conteúdo sensível/secrets nunca devem ser expostos | E-0025 | HIGH | MEDIUM | UX/observability task must define safe redaction/visibility model | Security/UX | OPEN_W005_RESEARCH |

## Risks

| ID | Risk | Likelihood | Impact | Trigger | Mitigation | Owner | Status |
|---|---|---|---|---|---|---|---|
| RISK-0001 | Drift factual em números/datas/entidades | MEDIUM | CRITICAL | claim sem support | factual backbone + source gate + fresh re-eval | Eval | STRONGLY_CONTROLLED_TESTED_SCOPE |
| RISK-0002 | Gaming de readability/jargão | MEDIUM | HIGH | métrica sobe, conceito cai | ACV + anti-gaming + required-concept checks | Eval | STRONGLY_REDUCED |
| RISK-0003 | Avaliação circular modelo→modelo ser tratada como human gold | MEDIUM | HIGH | automated label vira “humano” | D-0017 explicit class + `human_gold=false` + blind frozen set | Eval | CONTROLLED_CLAIM_BOUNDARY |
| RISK-0004 | Corpus pequeno não generaliza | HIGH | HIGH | métricas instáveis | expand/version corpus + held-out + production eval science | Eval | ACTIVE_PRODUCTION_BLOCKER |
| RISK-0005 | Retries elevam custo/latência | LOW-MEDIUM | MEDIUM | repeated quality repair | bounded targeted repair + telemetry | Architecture | CONTROLLED |
| RISK-0006 | Vídeo não prova uso real <=5min | LOW | CRITICAL | artifact ilegível/ausente | W004 closed; regenerate final video after production build | Demo | REOPEN_FINAL_PRODUCT_EVIDENCE |
| RISK-0007 | Overengineering sem ganho | MEDIUM | HIGH | framework lock sem evidence | DRG + current baseline + representative benchmark | Orchestrator | CONTROLLED_BY_DRG |
| RISK-0008 | Adaptação vira recomendação financeira nova | MEDIUM | HIGH | unsupported recommendation | policy/factual hard gates | Compliance | CONTROLLED_TESTED_SCOPE |
| RISK-0009 | Uma função de qualidade aplicada a todos formatos | LOW | MEDIUM | native contract falha | per-format contracts + slices | Eval/UX | CONTROLLED |
| RISK-0010 | Extração PDF perde role/unit/table context | MEDIUM | HIGH | source trust baixa | fail-closed source gate + expanded parser benchmark | Data | CONTROLLED_DETECTION_PARSER_IDENTITY_OPEN |
| RISK-0011 | Owner/workflow Suno desconhecido reduz adoção | MEDIUM | HIGH | proposta depende de processo presumido | manter UNKNOWN + modular adapters | Strategy | OPEN_EXTERNAL |
| RISK-0012 | main sem branch protection | MEDIUM | MEDIUM | push acidental | lease + PR discipline + integrity CI + checkpoints | Orchestrator | ACCEPTED_CONTROLLED |
| RISK-0013 | Join paralelo perde outputs | LOW | HIGH | overwrite | keyed identities + 9/9 lossless join + RunStore | Architecture | CLOSED_TESTED_SCOPE |
| RISK-0014 | Formatos curtos inflam readability | MEDIUM | MEDIUM | score artificial | ACV + anti-gaming + diagnostic-only thresholds | Eval | CONTROLLED |
| RISK-0015 | Ontologia/policy envelhece | MEDIUM | MEDIUM | drift | versioning + fixtures/regression | Eval/Compliance | CONTROLLED_PARTIAL |
| RISK-0016 | Demo parece enlatada | LOW | HIGH | sem source/input path | single real product path mandated by D-0018 | Demo/UX | CONTROLLED_NEW_SCOPE |
| RISK-0017 | Model/provider muda comportamento/custo | MEDIUM | MEDIUM | provider drift | provider-neutral harness + re-eval + routing evidence | Architecture | REDUCED_NO_OVERALL_LOCK |
| RISK-0018 | Componentes passam isolados e falham no clean checkout | LOW-MEDIUM | HIGH | integration drift | continuous E2E/release gates | Auditor | CONTROLLED_BASELINE_REVALIDATE_PRODUCTION |
| RISK-0019 | Custo sintético confundido com custo real | LOW | HIGH | pricing sem provenance | observed usage + versioned official pricing | Orchestrator | CONTROLLED |
| RISK-0020 | Ausência de human gold mascarada por confusion matrix circular | MEDIUM | HIGH | automated target chamado “human” | explicit evidence classes + production human calibration gate | Eval | CONTROLLED_CLAIM_BOUNDARY |
| RISK-0021 | Mechanics proof confundido com production readiness | HIGH | CRITICAL | internal PASS vira production claim | Production Contract + evidence class + scorecards | Orchestrator | ACTIVE_HARD_GATE |
| RISK-0022 | Credential/runtime impede provider evidence | LOW | HIGH | preflight fails | provider abstraction + observed prior path + secret management | Provider | CONTROLLED_PARTIAL |
| RISK-0023 | Pseudo-independência em futura amostra humana | MEDIUM | HIGH | mesma pessoa gera streams | explicit blind independent annotation/adjudication protocol | Eval | OPEN_PRODUCTION_DESIGN |
| RISK-0024 | Recipient app parece dashboard estático | HIGH | HIGH | preview mechanics-only/fake | final UI must consume real provider/workflow/events | UX/Data | ACTIVE_PRODUCTION_BLOCKER |
| RISK-0025 | Packet/README stale | MEDIUM | HIGH | product truth muda | regenerate docs/report from final production evidence | Writer/Auditor | ACTIVE_LATER |
| RISK-0026 | Actions video artifact expira | LOW | HIGH | retention expiry | durable repository/object artifact | Demo | CLOSED_W004 |
| RISK-0027 | BCB fail-closed parece produto quebrado | LOW | HIGH | blocked path mostrado primeiro | success-path-first + explicit negative-control UX | Demo/UX | CONTROLLED_REVIEW_SCOPE |
| RISK-0028 | 3×3 não cabe inteiro no viewport | MEDIUM | MEDIUM | visual row inspection | responsive matrix + filters/zoom/detail while preserving 9/9 proof | UX | OPEN_PRODUCTION_UX |
| RISK-0029 | Deadline/submission mechanism/finalization reserve desconhecidos impedem finalização formal | HIGH | CRITICAL | tentativa de marcar COMPLETE sem fatos | manter project ACTIVE + stop conditions FAIL | Orchestrator | OPEN_EXTERNAL_CRITICAL_FINALIZATION |
| RISK-0030 | Attempt reutilizado após terminal signal invalida provenance | LOW | HIGH | multiple terminals same attempt | fresh attempts + integrity/lease discipline | Orchestrator | CLOSED_BY_PROVENANCE_REPAIR |
| RISK-0031 | Cross-tenant data leakage | MEDIUM | CRITICAL | user/tenant acessa resource alheio | identity/tenant binding + authz + RLS/alternative DRG + adversarial tests; zero allowed | Security/Data | OPEN_P0 |
| RISK-0032 | Arbitrary server filesystem path/upload abuse | HIGH if current pattern exposed | CRITICAL | untrusted path/upload reaches server filesystem | remove arbitrary path from production boundary; controlled object upload + validation | Security/API | OPEN_P0 |
| RISK-0033 | SQLite/local state fails under multi-replica/multi-user runtime | HIGH | CRITICAL | concurrent replicas/shared state/restart | storage DRG + shared durable persistence + migration/recovery tests | Data/Architecture | OPEN_P0 |
| RISK-0034 | Stack chosen by fashion/preference creates unnecessary rewrite/lock-in | MEDIUM | HIGH | framework selected without representative evidence | mandatory DRG + baseline bakeoff + reversal conditions | Architecture | CONTROLLED_PROTOCOL_W005_OPEN |
| RISK-0035 | Frontend visualizes synthetic/stale evidence instead of live runtime | HIGH | HIGH | UI reads fixtures/manifests unrelated to current run | correlated run/event/trace IDs + live backend contract + provenance checks | UX/Observability | OPEN_P0_P1 |
| RISK-0036 | Production audience thresholds promoted from weak automated calibration | MEDIUM | CRITICAL | D-0017 reused beyond scope | PROD-008 requires stronger independent evidence; thresholds remain diagnostic | Eval | OPEN_P1 |
| RISK-0037 | Observability leaks sensitive documents/prompts/secrets | MEDIUM | HIGH | full payloads exported indiscriminately | telemetry redaction/classification + least exposure + security review | Security/Observability | OPEN_P0_P1 |
| RISK-0038 | Capacity target invented or untested | HIGH | HIGH | “supports N users” without load evidence | saturation curve + p50/p95/p99/error/queue/resource measurements | SRE | OPEN_P1 |
| RISK-0039 | Adaptive routing optimizes cost/latency by bypassing quality/safety | MEDIUM | CRITICAL | policy selects cheaper path despite hard fail | non-compensatory gates outside optimizer + policy tests + audit | AI/Eval | OPEN_P0_P1 |
| RISK-0040 | Research process vira documentação burocrática sem decision value | MEDIUM | MEDIUM | long docs, no benchmark/reversal | DRG stopping rule/evidence saturation + decision question + workload benchmark | Orchestrator | CONTROLLED_BY_PROTOCOL |

## Rules

- Assumptions usam `A-####`; risks usam `RISK-####`.
- Premissa de alto impacto + alta incerteza deve gerar validação, controle explícito ou permanecer external blocker.
- Uma premissa crítica não desaparece por consenso; só muda por evidência, mitigação ou decisão explícita.
- `PROJECT_STATUS: COMPLETE` exige nenhuma premissa crítica material `UNCONTROLLED` e todos os stop conditions do Success Model satisfeitos.
- `PRODUCTION_READY` exige zero P0 aberto do Production Contract no escopo do claim.
