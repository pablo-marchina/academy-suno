# ASSUMPTION & RISK REGISTER

## Assumptions

| ID | Assumption | Evidence | Impact if wrong | Uncertainty | Validation / mitigation | Owner | Status |
|---|---|---|---|---|---|---|---|
| A-0001 | Para o vídeo final, usar <=5:00 como regra operacional segura | E-0001,T019,T020,T021,T008-A02 | CRITICAL | LOW | final MP4 69.120s, independently reviewed and durable | Orchestrator | CONTROLLED |
| A-0002 | Usuário interno provável é conteúdo/editorial/research; owner real não identificado | E-0002 + inferência | HIGH | HIGH | não afirmar workflow interno; manter adapters modulares | Research | OPEN_EXTERNAL |
| A-0003 | Valor principal é `content transformation + trust layer`, não simples resumo | W001–W004; T020; T008-A02 | HIGH | MEDIUM | produto/demo + evidence layer executados; ROI real não alegado | Strategy | SUPPORTED_HYPOTHESIS |
| A-0004 | Níveis de sofisticação exigem calibração além de prompts | T005-A02; D-0017 | HIGH | MEDIUM | automated blind calibration aceita para este case; thresholds DIAGNOSTIC_ONLY; human sample opcional | Eval | CONTROLLED_CASE_WAIVER_NO_HUMAN_GOLD |
| A-0005 | Pydantic nas fronteiras + orchestration evidence-driven são adequados | W002,W003,T008-A02 | MEDIUM | LOW | clean E2E mechanics e persistent state observados | Architecture | SUPPORTED |
| A-0006 | Não há dataset gold/anotado fornecido pelo parceiro | briefing; T005-A02; D-0017 | HIGH | HIGH | waiver aceita MODEL_AUTOMATED_BLIND_CALIBRATION sem relabel humano | Eval | CONTROLLED_CASE_WAIVER_EXTERNAL_HUMAN_OPTIONAL |
| A-0007 | Imitação de voz Suno pode ser desejável, mas não é requisito hard do briefing | E-0001,E-0002 | MEDIUM | HIGH | manter opcional; não alegar style-transfer validado | Content | OPEN_NONCRITICAL |
| A-0008 | Documentos públicos-alvo podem ser parseados com fail-closed suficiente para demo | T014,T019,T020,T008-A02 | HIGH | LOW-MEDIUM | positive path + BCB ambiguity negative-control observados | Data | SUPPORTED_FAIL_CLOSED |
| A-0009 | Flesch PT-BR precisa implementação/teste controlado | W003,T005-A02 | MEDIUM | LOW | versioned implementation + diagnostics; no threshold freeze | Eval | SUPPORTED_IMPLEMENTED |
| A-0010 | Semantic/LLM judge deve ser sensor secundário, não árbitro único | W003,T006-A01 | HIGH | LOW | hard-gate non-compensation; zero measured gain → no backend lock | Eval | CONTROLLED_BY_DESIGN |
| A-0011 | Valor operacional real pode incluir tempo/retrabalho/reuso multicanal | inferência + telemetry/provider evidence | HIGH | HIGH | não emitir ROI claim sem baseline/owner/workflow Suno | Partner Research | OPEN_EXTERNAL_VALUE_MAGNITUDE |

## Risks

| ID | Risk | Likelihood | Impact | Trigger | Mitigation | Owner | Status |
|---|---|---|---|---|---|---|---|
| RISK-0001 | Drift factual em números/datas/entidades | MEDIUM | CRITICAL | claim sem support | factual backbone + source gate + fresh re-eval | Eval | STRONGLY_CONTROLLED_TESTED_SCOPE |
| RISK-0002 | Gaming de readability/jargão | MEDIUM | HIGH | métrica sobe, conceito cai | ACV + anti-gaming + required-concept checks | Eval | STRONGLY_REDUCED |
| RISK-0003 | Avaliação circular modelo→modelo ser tratada como human gold | MEDIUM | HIGH | automated label vira “humano” | D-0017 explicit class + `human_gold=false` + blind frozen set | Eval | CONTROLLED_CLAIM_BOUNDARY |
| RISK-0004 | Corpus pequeno não generaliza | HIGH | HIGH | métricas instáveis | six-source DEVELOPMENT + no threshold freeze + claims bounded | Eval | ACTIVE_ACCEPTED_SAMPLE_LIMIT |
| RISK-0005 | Retries elevam custo/latência | LOW-MEDIUM | MEDIUM | repeated quality repair | bounded targeted repair + telemetry | Architecture | CONTROLLED |
| RISK-0006 | Vídeo não prova uso real <=5min | LOW | CRITICAL | artifact ilegível/ausente | T019/T020/T021/T008-A02 exact durable 69.120s MP4 | Demo | CLOSED |
| RISK-0007 | Overengineering sem ganho | LOW | HIGH | framework lock sem evidence | T006 zero-gain result + no backend lock | Orchestrator | REDUCED |
| RISK-0008 | Adaptação vira recomendação financeira nova | MEDIUM | HIGH | unsupported recommendation | policy/factual hard gates | Compliance | CONTROLLED_TESTED_SCOPE |
| RISK-0009 | Uma função de qualidade aplicada a todos formatos | LOW | MEDIUM | native contract falha | per-format contracts + slices | Eval/UX | CONTROLLED |
| RISK-0010 | Extração PDF perde role/unit/table context | MEDIUM | HIGH | source trust baixa | fail-closed source gate + BCB negative-control | Data | CONTROLLED_DETECTION_PARSER_IDENTITY_OPEN |
| RISK-0011 | Owner/workflow Suno desconhecido reduz adoção | MEDIUM | HIGH | proposta depende de processo presumido | manter UNKNOWN + modular adapters | Strategy | OPEN_EXTERNAL |
| RISK-0012 | main sem branch protection | MEDIUM | MEDIUM | push acidental | lease + PR discipline + integrity CI + checkpoints | Orchestrator | ACCEPTED_CONTROLLED |
| RISK-0013 | Join paralelo perde outputs | LOW | HIGH | overwrite | keyed identities + 9/9 lossless join + RunStore | Architecture | CLOSED_TESTED_SCOPE |
| RISK-0014 | Formatos curtos inflam readability | MEDIUM | MEDIUM | score artificial | ACV + anti-gaming + diagnostic-only thresholds | Eval | CONTROLLED |
| RISK-0015 | Ontologia/policy envelhece | MEDIUM | MEDIUM | drift | versioning + fixtures/regression | Eval/Compliance | CONTROLLED_PARTIAL |
| RISK-0016 | Demo parece enlatada | LOW | HIGH | sem source/input path | real recipient app/browser capture + independent review | Demo | CLOSED_REVIEW_SCOPE |
| RISK-0017 | Model/provider muda comportamento/custo | MEDIUM | MEDIUM | provider drift | provider-neutral harness + T004 A08 + T007 A05 bounded comparison | Architecture | REDUCED_NO_OVERALL_LOCK |
| RISK-0018 | Componentes passam isolados e falham no clean checkout | LOW | HIGH | integration drift | T012 + attempt-valid T008-A02 clean E2E | Auditor | CLOSED_INTERNAL_RELEASE_PROOF |
| RISK-0019 | Custo sintético confundido com custo real | LOW | HIGH | pricing sem provenance | observed usage + versioned official pricing in accepted provider evidence | Orchestrator | CONTROLLED |
| RISK-0020 | Ausência de human gold mascarada por confusion matrix circular | MEDIUM | HIGH | automated target chamado “human” | explicit automated matrices/class; no human claims | Eval | CONTROLLED_CLAIM_BOUNDARY |
| RISK-0021 | Mechanics proof confundido com production readiness | MEDIUM | CRITICAL | internal PASS vira production claim | evidence classes + T008 blanket-production false + scorecards | Orchestrator | CONTROLLED |
| RISK-0022 | Credential/runtime impede provider evidence | LOW | HIGH | preflight fails | A08 official-compatible client observed; A05 comparison observed | Provider | CLOSED |
| RISK-0023 | Pseudo-independência em futura amostra humana | MEDIUM | HIGH | mesma pessoa gera streams | T009 session/provenance rules remain mandatory if human claim is ever added | Eval | DORMANT_OPTIONAL_HUMAN_ENHANCEMENT |
| RISK-0024 | Recipient app parece dashboard estático | LOW | HIGH | sem ingest real | T014 + T019 + T020 | UX/Data | CLOSED_REVIEW_SCOPE |
| RISK-0025 | Packet/README stale | LOW | HIGH | evaluator vê truth antiga | T019 refresh + T020 review + T008 current evidence | Writer/Auditor | CONTROLLED_CURRENT_INTERNAL_PACKAGE |
| RISK-0026 | Actions video artifact expira | LOW | HIGH | retention expiry | T021 durable repository exact copy | Demo | CLOSED |
| RISK-0027 | BCB fail-closed parece produto quebrado | LOW | HIGH | blocked path mostrado primeiro | success-path-first + explicit negative-control + independent review | Demo/UX | CLOSED_REVIEW_SCOPE |
| RISK-0028 | 3×3 não cabe inteiro no viewport | MEDIUM | MEDIUM | visual row inspection | 9/9 caption + DOM/artifact binding | Demo/UX | ACCEPTED_PRESENTATION_REFINEMENT |
| RISK-0029 | Deadline/submission mechanism/finalization reserve desconhecidos impedem finalização formal | HIGH | CRITICAL | tentativa de marcar COMPLETE sem fatos | manter project ACTIVE + stop conditions FAIL até verificação externa | Orchestrator | OPEN_EXTERNAL_CRITICAL_FINALIZATION |
| RISK-0030 | Attempt reutilizado após terminal signal invalida provenance | LOW | HIGH | multiple terminals same attempt | A02 demoted, A05 fresh attempt accepted, integrity/lease discipline reinforced | Orchestrator | CLOSED_BY_PROVENANCE_REPAIR |

## Rules

- Assumptions usam `A-####`; risks usam `RISK-####`.
- Premissa de alto impacto + alta incerteza deve gerar validação, controle explícito ou permanecer external blocker.
- Uma premissa crítica não desaparece por consenso; só muda por evidência, mitigação ou decisão explícita.
- `PROJECT_STATUS: COMPLETE` exige nenhuma premissa crítica material `UNCONTROLLED` e todos os stop conditions do Success Model satisfeitos.
