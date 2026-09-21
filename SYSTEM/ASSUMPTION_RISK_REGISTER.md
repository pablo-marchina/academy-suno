# ASSUMPTION & RISK REGISTER

## Assumptions

| ID | Assumption | Evidence | Impact if wrong | Uncertainty | Validation / mitigation | Owner | Status |
|---|---|---|---|---|---|---|---|
| A-0001 | Para o vídeo final, a regra operacional deve ser <=5:00 apesar de o Entregável 5 mencionar “5 a 7 minutos” | E-0001,E-0013,E-0015,E-0016,E-0017,E-0018 | CRITICAL | MEDIUM | T019 produziu 69.12s; T020 remeasure/independent review PASS; confirmar com organizador se houver canal | Orchestrator | CONTROLLED_OPERATIONALLY_VIDEO_REVIEW_PASS |
| A-0002 | O usuário interno provável é equipe de conteúdo/editorial/research, mas owner/decision maker não foram identificados | E-0002 + inferência | HIGH | HIGH | não projetar workflow final como fato | Research | OPEN |
| A-0003 | O maior valor é `content transformation + trust layer`, não “resumidor” | E-0001,E-0002,W001,W002,W003,W004-T001,E-0018 | HIGH | MEDIUM | medir incrementality contra prompt/simple/manual em representative runs | Strategy | SUPPORTED_HYPOTHESIS |
| A-0004 | Níveis de sofisticação precisam de gold/calibração mensurável além de prompts | W003-T001/T004/T008/T009;W004-T002 | HIGH | LOW | frozen blind development set + agreement tooling prontos; T005 mede human gold/agreement | Eval | SUPPORTED_PREPARATION_PASS_THRESHOLD_OPEN |
| A-0005 | Pydantic é adequado às fronteiras persistidas; orchestration final deve ser evidence-driven | W002;W003-T003/T009 | MEDIUM | LOW | plain async executou E2E mechanics; LangGraph challenger é opcional/non-blocking | Architecture | PLAIN_ASYNC_PROVISIONAL_EVIDENCE_LEADER |
| A-0006 | Não foi fornecido dataset gold/anotado pelo parceiro | briefing; W003-T001/T008/T009;W004-T002 | HIGH | HIGH | W004 corpus + T009 annotation operator concluídos; T005 requer duas pessoas realmente independentes e held-out protegido | Eval | PARTIALLY_MITIGATED_ANNOTATION_READY_HUMAN_GOLD_OPEN |
| A-0007 | Imitação de “voz Suno” pode ser desejável, mas briefing exige níveis, não style transfer de marca | E-0001,E-0002,W001-T001 | MEDIUM | HIGH | manter soft/opcional até evidência interna | Content | OPEN |
| A-0008 | Documentos públicos-alvo podem ser parseados de forma confiável suficiente para demo | W002-T002/T007/T010;W003-T009;W004-T003;E-0014,E-0015,E-0016,E-0017,E-0018 | HIGH | MEDIUM | T014/T019 provaram raw ingest; T020 confirmou success path + BCB fail-closed; parser identity continua unlocked | Data | SUPPORTED_DEMO_PATH_FAIL_CLOSED_PARSER_IDENTITY_UNLOCKED |
| A-0009 | Flesch PT-BR requer implementação/teste controlado em vez de uso cego de biblioteca genérica | W003-T004/T008 | MEDIUM | LOW | `ptbr-readability-v001` + tests + anti-gaming gate; thresholds diagnósticos | Eval | SUPPORTED_IMPLEMENTED |
| A-0010 | LLM/semantic judge deve ser sensor secundário e estruturado, não árbitro único | W003-T002/T006/T008/T009 | HIGH | LOW | hard-gate non-compensation executável; W004-T006 mede valor incremental após T005 | Eval | CONTROLLED_BY_DESIGN |
| A-0011 | Ganho operacional real do parceiro pode incluir tempo/retrabalho/reuso multicanal | E-0002 + inferência; W003 telemetry; W004 cockpit/provider harness | HIGH | HIGH | real provider + human evidence + baseline comparison antes de ROI claim | Partner Research | OPEN_INSTRUMENTED_COCKPIT_READY |

## Risks

| ID | Risk | Likelihood | Impact | Trigger | Mitigation | Owner | Status |
|---|---|---|---|---|---|---|---|
| RISK-0001 | Alucinação/drift factual em números, datas, entidades, direção/condicionais | HIGH | CRITICAL | claim sem source support | factual backbone + claim grounding + fresh source/factual/policy re-eval after repair | Eval | STRONGLY_CONTROLLED_CORE |
| RISK-0002 | Gaming: melhorar readability apagando conceito ou inflar densidade com jargão | HIGH | HIGH | métrica sobe enquanto cobertura cai | mandatory anti-gaming gate + independent human calibration downstream | Eval | STRONGLY_REDUCED_GATE_PASS |
| RISK-0003 | Avaliação circular: mesmo modelo gera e valida sem ground truth | MEDIUM | HIGH | target/prediction vira gold | frozen blind bank, target hidden from primaries, held-out rejection + T005 independent humans | Eval | STRONGLY_REDUCED_HUMAN_GOLD_OPEN |
| RISK-0004 | Dataset pequeno/desbalanceado não generaliza | HIGH | HIGH | métricas instáveis por slice | expanded 6-source corpus, source-level split, 36 development outputs, no threshold freeze; stronger 18-doc target retained | Eval | REDUCED_BUT_ACTIVE_SAMPLE_LIMIT |
| RISK-0005 | Retries aumentam custo/latência e não convergem | MEDIUM | MEDIUM | >stop criteria ou piora após repair | targeted repair bounded stops + separate telemetry; real-model evidence W004 | Architecture | STRONGLY_REDUCED_CORE_REAL_MODEL_OPEN |
| RISK-0006 | Vídeo não prova funcionamento real <=5 min ou é insuficiente para avaliador | LOW | CRITICAL | artifact ausente, >5 min, ilegível ou não reproduzível | T019 real paced 69.12s + T020 direct independent artifact review PASS + T021 durable byte-identical repository copy | Demo | STRONGLY_CONTROLLED_VIDEO_PACKAGE_AND_DURABILITY_PASS |
| RISK-0007 | Overengineering consome tempo sem melhorar critérios | LOW | HIGH | framework sofisticado sem ganho | no framework rewrite; plain async evidence leader | Orchestrator | REDUCED |
| RISK-0008 | Conteúdo cruza adaptação e vira recomendação financeira nova | MEDIUM | HIGH | recommendation nova/personalização | canonical policy hard gates + post-repair re-eval | Compliance | CONTROLLED_CORE |
| RISK-0009 | Uma função de qualidade é aplicada indevidamente a todos os formatos | LOW-MEDIUM | MEDIUM | texto passa, mídia falha | native format contracts + format slicing + independent human calibration | Eval/UX | CONTROLLED_FOUNDATION |
| RISK-0010 | Extração PDF perde tabelas/números/rodapés | MEDIUM | HIGH | source-trust baixa | role-aware source gate catches wrong-role/unit corruption; T014/T019/T020 confirm fail-closed behavior; no demo bypass | Data | REDUCED_DETECTION_STRONG_PARSER_LOCK_OPEN |
| RISK-0011 | Owner/workflow interno desconhecido leva a proposta pouco adotável | MEDIUM | HIGH | solução depende de processo não evidenciado | modular adapters + partner jury | Strategy | OPEN |
| RISK-0012 | `main` sem branch protection por decisão do usuário | MEDIUM | MEDIUM | push direto acidental | CI, lease, PR discipline, checkpoints | Orchestrator | ACCEPTED |
| RISK-0013 | Estado paralelo perde outputs silenciosamente | LOW | HIGH | join sobrescreve branch | keyed job identity + W003 E2E 9/9 lossless join + RunStore reopen/resume | Architecture | STRONGLY_CONTROLLED_E2E |
| RISK-0014 | Formatos curtos inflam readability artificialmente | HIGH | MEDIUM | readability sobe sem mudança cognitiva | ACV + anti-gaming + human calibration | Eval | STRONGLY_REDUCED_GATE_PASS |
| RISK-0015 | Ontologia/policy envelhece e aliases/regras divergem | MEDIUM | MEDIUM | regressão por mudança | versionamento + fixtures + clean regression | Eval/Compliance | CONTROLLED_PARTIAL |
| RISK-0016 | Fallback/demo parece conteúdo enlatado e não prova execução real | LOW | HIGH | demo sem input/source/evidence path real | T019 success-path-first real browser evidence + T020 independent frame/artifact review | Demo | STRONGLY_CONTROLLED_VIDEO_PACKAGE_SCOPE |
| RISK-0017 | Mudança de model/provider altera comportamento/custo | HIGH | MEDIUM | provider drift | provider-neutral harness + explicit N/A/pricing provenance; real comparable runs still required | Architecture | REDUCED_HARNESS_READY_REAL_RUN_BLOCKED |
| RISK-0018 | Componentes passam isoladamente mas falham em clean combined checkout | LOW | HIGH | task-specific integration não executa em release CI | T012 clean release smoke + T019 real browser CI; T008 final gate remains | Auditor | STRONGLY_REDUCED_CLEAN_RELEASE_PASS |
| RISK-0019 | Custo sintético de demo ser confundido com custo real | MEDIUM | HIGH | synthetic pricing aparece sem provenance | provider harness rejects synthetic pricing for commercial cost; cockpit preserves N/A | Orchestrator | STRONGLY_CONTROLLED |
| RISK-0020 | Ausência de human gold ser mascarada por confusion matrix circular | MEDIUM | HIGH | requested target usado como truth | blind bank hides target; two independent primaries required; T005 kill criterion blocks pseudo-human gold | Eval | STRONGLY_CONTROLLED_PREP_HUMAN_LABELS_PENDING |
| RISK-0021 | Mechanics proof ser confundido com provider/model-quality ou production-readiness proof | MEDIUM | CRITICAL | deterministic/CI mechanics usados em claim externo | cockpit states + T020 scope-specific PASS wording + provider harness + final T008 gate | Orchestrator | STRONGLY_REDUCED_GUARDRAILS_ACTIVE |
| RISK-0022 | Runtime/credencial autorizada de provider indisponível impede evidência real de quality/latency/usage/cost | MEDIUM | HIGH | provider task retorna no-credential/blocker | T010 manual workflow secret-safe + strict importer prontos; ainda requer secret/runtime autorizado | Orchestrator/Provider | MITIGATED_PATH_READY_EXTERNAL_BLOCKER_OPEN |
| RISK-0023 | Duas streams de anotação parecem independentes no formato mas não vêm de duas pessoas realmente independentes | MEDIUM | HIGH | mesma pessoa/processo produz A e B | T009 separa roles/sessions/provenance e proíbe cross-import; independência física deve ser atestada antes de T005 | Eval/Orchestrator | OPEN_EXTERNAL_VALIDITY_GATE |
| RISK-0024 | Pacote recipient-facing parece dashboard estático e não demonstra ingestão real | LOW | HIGH | avaliador não encontra upload/input PDF/texto nem interação clara | T014 app + T019 recording + T020 independent review | UX/Data | CONTROLLED_REVIEW_SCOPE_PASS |
| RISK-0025 | Evidência fica fragmentada ou packet/README ficam temporalmente stale | LOW | HIGH | evaluator sees pre-remediation truth | T019 refreshed packet/root README; T020 independently verified currency; T021 added durable artifact provenance pointer | Writer/Auditor | CONTROLLED_CURRENT_PACKAGE_REVIEWED |
| RISK-0026 | Actions artifact de vídeo expira antes da avaliação/submissão | LOW | HIGH | accepted Actions artifact expires | T021 copied exact accepted MP4 to `artifacts/submission/final-demo.mp4`, verified SHA/size before persistence and fresh-clone SHA/size + `cmp` after push | Orchestrator/Demo | CLOSED_DURABLE_REPOSITORY_COPY_PASS |
| RISK-0027 | Fail-closed BCB PDF pode parecer “produto quebrado” sem framing | LOW | HIGH | final demo leads with SOURCE_BLOCKED state or hides why it blocked | T019 success path first + explicit negative-control; T020 cold-evaluator review PASS | Demo/UX | STRONGLY_CONTROLLED_VIDEO_PACKAGE_SCOPE |
| RISK-0028 | 9 linhas do 3×3 de sucesso não cabem simultaneamente no viewport do vídeo | MEDIUM | MEDIUM | avaliador exige inspeção visual linha-a-linha sem usar caption/DOM evidence | 9/9 caption + DOM/artifact binding + review note; considerar traversal apenas se submission reviewer exigir | Demo/UX | ACCEPTED_PRESENTATION_REFINEMENT |

## Rules

- Assumptions usam `A-####`; risks usam `RISK-####`.
- Premissa de alto impacto + alta incerteza deve gerar task de validação/teste.
- Uma premissa crítica não pode desaparecer por consenso; só muda por evidência, mitigação ou decisão explícita.
- `PROJECT_STATUS: COMPLETE` exige nenhuma premissa crítica material `UNCONTROLLED`.
