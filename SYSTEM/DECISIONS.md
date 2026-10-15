# DECISION LOG

Somente o Orchestrator com lease ativo pode alterar este arquivo.

## D-0001 — GitHub como fonte canônica
- Status: `LOCKED`
- Estado de origem: `STATE-v0001`
- Decisão: GitHub é fonte de verdade.

## D-0002 — Escrita exclusiva do Orchestrator
- Status: `LOCKED`
- Estado de origem: `STATE-v0001`
- Decisão: workers não atualizam canônicos.

## D-0003 — Waves paralelas versionadas
- Status: `LOCKED`
- Estado de origem: `STATE-v0001`
- Decisão: tarefas independentes são paralelizadas com base explícita.

## D-0004 — Guardrails executáveis
- Status: `LOCKED`
- Estado de origem: `STATE-v0003`
- Decisão: CI/ownership/PR protegem governança.

## D-0005 — Lease atômico exclusivo
- Status: `LOCKED`
- Estado de origem: `STATE-v0004`
- Decisão: somente holder do lease integra estado.

## D-0006 — Proveniência por tentativa
- Status: `LOCKED`
- Estado de origem: `STATE-v0004`
- Decisão: toda execução usa TASK+ATTEMPT+BASE_STATE+BASE_COMMIT.

## D-0007 — Checkpoints e DAG
- Status: `LOCKED`
- Estado de origem: `STATE-v0004`
- Decisão: mudanças de estado têm snapshot; waves têm DAG.

## D-0008 — Qualidade do case como função única
- Status: `SUPERSEDED`
- Estado de origem: `STATE-v0005`
- Superseded by: `D-0012`.

## D-0009 — Loop obrigatório
- Status: `LOCKED`
- Estado de origem: `STATE-v0005`
- Decisão: projeto itera até hard gates/stop condition.

## D-0010 — Partner Value como função primária isolada
- Status: `SUPERSEDED`
- Estado de origem: `STATE-v0006`
- Superseded by: `D-0012`.

## D-0011 — Partner Contract/Jury/Adoption Gate
- Status: `LOCKED`
- Estado de origem: `STATE-v0006`
- Decisão: utilidade real, adoção e counterfactuals são obrigatórios.

## D-0012 — Balanced Total Success é a função objetivo dominante
- Status: `LOCKED`
- Estado de origem: `STATE-v0007`
- Decisão: sucesso é multiobjetivo com hard gates: Partner Outcome, fit ao briefing/avaliação, evidência/rigor, solução/diferenciação, viabilidade/adoção, excelência do deliverable, comunicação/defesa e robustez de execução. Nenhum score alto compensa hard gate crítico.
- Motivo: a melhor entrega resulta da combinação, não de otimizar uma dimensão isolada.

## D-0013 — Traceability e critical assumptions são gates
- Status: `LOCKED`
- Estado de origem: `STATE-v0007`
- Decisão: requisito/pain/claim material deve ser rastreável até evidência/solução/métrica/artefato; premissa high-impact/high-uncertainty precisa ser validada ou controlada.

## D-0014 — Blind Final Review e deadline reserve são obrigatórios
- Status: `LOCKED`
- Estado de origem: `STATE-v0007`
- Decisão: material final é avaliado sem contexto interno e o scheduler reserva tempo para integração, QA, defesa e submissão.

## D-0015 — Lifecycle de worker é observável por sinais duráveis
- Status: `LOCKED`
- Estado de origem: `STATE-v0010`
- Decisão: toda tentativa de worker despachada em protocolo 1.6.0+ registra `TASK_STARTED` antes do trabalho substantivo e exatamente um terminal `TASK_COMPLETE`, `TASK_BLOCKED` ou `TASK_STALE` na Issue; `TASK_PROGRESS` é opcional em marcos materiais. O Orchestrator deriva runtime status dos sinais + artefatos, e somente ele atualiza status canônico.
- Motivo: eliminar a dependência do usuário para informar se chats foram abertos/terminaram e distinguir `READY` de `RUNNING` sem depender da memória da conversa.
- Guardrail: não usar heartbeat periódico/TTL como prova de liveness; chats não são processos confiáveis em background. Branch/commits/results são evidência secundária e attempts novos nunca são reutilizados.

## D-0016 — Foundation invariants lockados; implementação permanece evidence-driven
- Status: `LOCKED`
- Estado de origem: `STATE-v0016`
- Decisão: ficam lockados os invariantes comprovados em W002 — typed Python + Pydantic v2 nas fronteiras persistidas, canonical source/provenance spine, source-trust antes de generation, semantic table-role provenance para fatos de tabela, factual/policy/source hard gates não compensatórios, 3 audiências × 3 formatos nativos, branch identity/job_id estáveis, repair local e semantic/LLM judge apenas como sensor secundário. Plain async é o líder provisório por runtime evidence; LangGraph permanece challenger até runtime recheck. Parser library, provider/model, semantic backend e audience thresholds continuam desbloqueados até evidência específica.
- Motivo: W002-T010 reconciliou EXP-A/B/C e separou `foundation proven`, `pending experiment` e `production unknown`, evitando locks por preferência.
- Guardrail: qualquer mudança nesses invariantes exige evidência material de ganho e não pode enfraquecer `CRIT-001`.

## D-0017 — Waiver explícito para calibração automatizada cega em W004
- Status: `LOCKED`
- Estado de origem: `STATE-v0034`
- Tipo: `EVIDENCE_SUBSTITUTION_WAIVER`
- Autorização: operador autorizou explicitamente substituir o blocker de duas streams humanas pela validação automatizada cega completa e continuar o Autopilot.
- Evidência aceita: `artifacts/evals/w004/model_validation_a03.jsonl` + provenance/summary, Actions run `35668224695`, 36/36 itens únicos, `MODEL_AUTOMATED`, Groq `openai/gpt-oss-120b`, blind leakage guardrails PASS, fresh-clone byte identity PASS, output SHA-256 `adae7376415cd7052b8b2b84002ce0a7a5890047cb86e98dbe456747c7fe1bb4`.
- Decisão: para o escopo `W004-T005 → W004-T006/W004-T007 → W004-T008`, a evidência A03 pode satisfazer a dependência de calibração que originalmente exigia human gold, desde que todos os artifacts/results downstream preservem a classe `MODEL_AUTOMATED_BLIND_CALIBRATION` e suas limitações.
- Claims proibidos: não declarar human gold, human agreement, human preference, audience validation por humanos, produção validada por humanos ou equivalentes. `human_gold_eligible=false` continua verdadeiro.
- Thresholds: audience thresholds permanecem `DIAGNOSTIC_ONLY`; nenhum threshold de produção pode ser lockado com A03 sozinho.
- T006: semantic-off/on pode usar A03 como reference calibration set para ablation diagnóstica, preservando hard gates; backend preference só pode ser lockada se o ganho for reprodutível no escopo automatizado e descrito como tal, nunca como preferência humana.
- T007: provider/model quality comparison pode usar source-grounded checks + A03 para comparação automatizada cega, junto de mechanics/custo/latência observados; qualquer winner/preference deve ser qualificado como `AUTOMATED_EVIDENCE_ONLY` e somente se datasets/configs forem comparáveis.
- Completion posture: a ausência de duas anotações humanas deixa de ser hard blocker deste case e passa a risco residual controlado, desde que os scorecards/risks preservem a limitação e nenhum claim final dependa de human agreement. Uma amostra humana futura é melhoria opcional, não dependência de execução.
- Motivo: o gate humano bloqueava todo o critical path apesar de existir uma avaliação cega completa, rastreável e reproduzível; o operador escolheu explicitamente a troca entre velocidade/autonomia e força da evidência. O waiver mantém integridade sem fabricar humanos.

## D-0018 — Production-grade Autopilot + systematic Decision Research Gate
- Status: `LOCKED`
- Estado de origem: `STATE-v0040`
- Tipo: `OPERATOR_SCOPE_EXPANSION`
- Autorização: o operador solicitou explicitamente elevar o projeto de case/demo-grade para a melhor entrega possível orientada a produção, com múltiplos usuários, quantitativo-first, Eval-Driven Development, adaptação onde segura, máxima visualização live no frontend e pesquisa sistemática/data-driven para qualquer escolha material.
- Decisão: introduzir `SYSTEM/PRODUCTION_CONTRACT.md` e `SYSTEM/DECISION_RESEARCH_GATE.md` como contratos obrigatórios do Autopilot. O W004 permanece evidência histórica válida do case, mas deixa de ser o target final de engenharia.
- Demo: “sem demo” é interpretado como “sem sistema fake/descartável exclusivo para demo”. O vídeo obrigatório do briefing continua <=5:00 e deve demonstrar o mesmo produto real.
- Research gate: nenhuma escolha material de stack/arquitetura/modelo/provider/parser/eval/auth/storage/deploy/observability/security pode virar production default/LOCKED sem pesquisa sistemática + alternatives + workload benchmark quando testável + limitations + reversal conditions.
- Quantitative-first: propriedades mensuráveis devem ser instrumentadas; thresholds não podem ser inventados. Hard gates não são compensatórios.
- Adaptive policy: adaptação é preferida para otimização (routing/model/prompt/retrieval/repair/budget/concurrency) somente quando telemetrada e incapaz de relaxar source/factual/policy/schema/provenance/authz/tenant hard gates.
- Multi-user: auth, tenant/workspace binding, RBAC/authz, shared durable state, secure uploads, observability, reliability e deployment evidence tornam-se hard requirements antes de qualquer `PRODUCTION_READY` claim.
- Calibration: D-0017 continua válido apenas para fechamento do W004. Para production audience thresholds/claims fortes, o novo Production Contract volta a exigir evidência humana independente ou evidence class equivalente explicitamente justificada sem falsificar human claims.
- Implementation posture: preservar componentes W001–W004 que passem DRG/benchmarks; reescrita por moda é proibida. Plain async atual é baseline obrigatório nos bakeoffs de orchestration.
- Next: abrir nova fase/wave de production research + architecture synthesis antes de congelar stack e depois desenvolver incrementalmente sob eval/regression gates.

## D-0019 — Waiver de evidência para operação AI-only sem avaliadores humanos
- Status: `LOCKED`
- Estado de origem: `STATE-v0066`
- Tipo: `EVIDENCE_SUBSTITUTION_WAIVER`
- Autorização: operador declarou expressamente que não haverá avaliadores humanos e instruiu a usar IA para avaliação; decisão válida para a nova trilha AI-only a partir da W009, não aplica retroativamente rótulos humanos às tentativas anteriores.
- Evidência alternativa permitida: `MODEL_AUTOMATED_BLIND_CALIBRATION`, `AI_JUDGE_SECONDARY`, `SOURCE_GROUNDED_EVIDENCE` e checagens determinísticas; cada registro guarda versão, origem, cegamento, dataset/corpus, resultado real e incerteza. Avaliação por LLM não pode compensar hard gate de fonte/fato/política/esquema/tenancy/proveniência.
- Escopo de downstream autorizado: diagnóstico automatizado, benchmark offline, otimização/ablation, prova de conceito e conteúdos explicitamente classificados com limitação de audiência, sob contratos de origem e segurança existentes. Não cria mecanismo para burlar os requisitos fortes de produção.
- Claims proibidos: `HUMAN_GOLD`, acordo humano, adjudicação humana, compreensão/preferência humana observada, generalização a leitores reais, limiares de audiência validados por humanos ou `PROD-008 PASS` com base apenas em LLM.
- Classificação obrigatória: `human_gold_eligible=false`, thresholds de audiência `DIAGNOSTIC_ONLY`, `HUMAN_EVIDENCE=UNAVAILABLE_BY_OPERATOR_CHOICE`, produção `FALSE/NOT_AUTHORIZED` até prova de todos os gates aplicáveis.
- Risco residual: viés/erro correlacionado de modelos, inferência sem leitor real, qualidade editorial sem parceiro; deve constar dos deliverables. Recuperação futura somente com avaliação humana de fato, se opção reconsiderada.
- Compatibilidade: D-0017 continua limitada à W004; W007-T005-A01 permanece `BLOCKED` imutável e não se torna PASS; novos AI-only workers usam novos IDs. Não desbloquear W007-T006/T010 automaticamente.
- Evidência de autorização: instrução explícita do operador em 2026-10-15; `docs/product/OPERATOR_SCOPE_AI_ONLY_RAILWAY_SUPABASE.md`.

## D-0020 — Railway/Supabase como escopo preferido de pesquisa de implantação
- Status: `PENDING_EVIDENCE` (diretriz do operador, NÃO tecnologia `LOCKED`)
- Estado de origem: `STATE-v0066`
- Tipo: `OPERATOR_PLATFORM_RESEARCH_DIRECTIVE`
- Autorização: operador solicitou usar integrações Railway/Supabase em vez de contratar GCP/AWS para execução atual.
- Alternativas: baseline local W006; Railway app/worker + Railway PostgreSQL; Railway app/worker + Supabase PostgreSQL/Auth/Storage; Supabase Edge Functions + PostgreSQL como counterfactual sujeito aos hard gates do Python e durable workflow. Histórico das alternativas GCP/AWS W007-T001 preservado sem fabricação de execução.
- Critério de promoção: `SYSTEM/DECISION_RESEARCH_GATE.md` completo, evidência real de execução no escopo, 3×3, auth/tenant isolado, source trust, durable event/outbox, backup/restart/restore, segurança, métricas brutas de carga, custo/latência/observabilidade, documentação de reversão. Resultado `NO_PREFERENCE` é permitido.
- Evidência externa atual: conexão dos provedores consultável; criação de novo projeto isolado na Railway não foi autorizada pelo provedor porque o trial expirou e é exigido um plano. Não houve deploy. Supabase requer confirmação de organização e custos para projeto novo; projetos de outros trabalhos não serão reutilizados sem autorização.
- Autoridade W007: W007-T002-A01 e W007-T005-A01 permanecem `BLOCKED` terminais; protocolo original T001 com três ambientes GCP/AWS não é substituído silenciosamente. Qualquer replanejamento do DAG/W007 exigirá nova decisão, nova tentativa/identidade, CI e checkpoint; W009-T002 só pesquisa a alternativa.
- Risco residual: dependência de uma ou duas plataformas, disponibilidade/faturamento, conexão segura, compatibilidade de pool, RLS e backup/PITR; gastos e credenciais não são assumidos.

## D-0021 — Ambiente Neon gratuito exclusivo, Railway limitado ao Free

- Status: `LOCKED` **somente na autorização de ambiente e limite de gastos**; **production technology decision = PENDING_EVIDENCE**.
- Estado de origem: `STATE-v0067`.
- Tipo: `OPERATOR_FREE_ONLY_INFRASTRUCTURE_AUTHORIZATION`.
- Autorização: operador autorizou criar um projeto novo, exclusivo para Academy Suno, no Supabase **ou** Neon, e usar **somente um plano gratuito** do Railway. Não autorizou contratar ou migrar para Railway Hobby/Pro, novas cobranças ou modificar projetos de outras iniciativas.
- Observação executada: organização Neon `org-noisy-truth-74026494` tinha `plan=free`; foi criado o projeto isolado `academy-suno`, ID `cold-math-95888995`, PostgreSQL 17 em `aws-sa-east-1`, banco `academy_suno`. Branch `main` em estado `ready` e query read-only de conectividade PASS, sem schema de produto, migração, deploy, usuário ou dados importados.
- Railway: tentativa de criar projeto privado de staging na conta existente retornou exatamente `Your trial has expired. Please select a plan to continue using Railway.`; nenhum projeto/serviço foi criado ou plano pago contratado. Apenas habilitar `Free` se o provider permitir; caso contrário `BLOCKED_BY_FREE_PLAN_UNAVAILABLE`.
- Segurança: credenciais, DSNs, chaves e segredos proibidos em documentos/commits/logs. Banco criado não é prova de autenticação de aplicação, tenant isolation, segurança de rede, backup/restore, RTO/RPO, throughput ou production readiness.
- DRG: ampliar contrafactual W009-T002 de D-0020 para incluir Railway App/Workers + Neon Free PostgreSQL, junto das opções anteriores; Neon é candidato para experimentação e **não** vencedor de produção. Completar DRG e testes representativos antes de qualquer default/LOCK.
- Limitações: quota efetiva/limites de compute, suspensão e billing devem ser monitorados. Plano Free não autoriza afirmar custo operacional real `0`; a tentativa de definir timeout de suspensão foi recusada pelo provedor, então o valor default não prova economia.
- Autoridade: W007-T002-A01/W007-T005-A01 continuam `BLOCKED` imutáveis, dependentes W007 não são liberados, D-0019 AI-only continua com `human_gold_eligible=false` e `PRODUCTION_READY=FALSE`.
- Evidência: `docs/production/NEON_FREE_STAGING_2026-10-15.md`, observações diretas de integrações Neon e Railway em 2026-10-15.

## D-0022 — Render Free como candidato limitado a staging técnico seguro

- Status: `LOCKED` apenas como autorização de **testar serviço Render Free** no workspace aprovado; `PENDING_EVIDENCE` para escolha de hosting de produção.
- Estado de origem: `STATE-v0068`.
- Tipo: `OPERATOR_APPROVED_FREE_STAGING_DEPLOYMENT`.
- Autorização: o operador confirmou explicitamente o workspace `Pablo's workspace` (ID `tea-db8g1d6q1p3s73d8k10g`) e a criação de serviço dedicado `academy-suno` **exclusivamente no plano gratuito**. Não autoriza Render Starter, Postgres/KeyValue pagos, plano empresarial, custos de tráfego excedente ou substituição de hard gates de produção.
- Security gate: a app reference `app/recipient/server.py` contém campo de caminho local PDF e não dispõe de identidade/isolamento de produção. **Proibido publicá-la diretamente**. A única superfície aprovada para o primeiro serviço é `app/hosting/render_staging.py` (diagnóstico HTTP read-only; endpoint `/readyz` sempre 503; sem upload/escrita, sem arquivos privados, sem credenciais/Neon).
- Evidência exigida para finalizar provisionamento: code/CI aprovado, confirmação de Render `plan=free`, deploy real `live`, logs, URL, resposta `/healthz` e falha fechada de `/readyz`/POST. Criar serviço sem observar deploy `live` não é implantação concluída.
- Benefício/limite: comprova boot HTTP e versão do contrato Python 3×3 definido, não gera outputs reais, não usa provider IA, não conecta ao Neon, não comprova failover/autenticação/produção; o serviço pode hibernar no Free.
- Adoção futura de Render + Neon requer comparação W009-T002/DRG, autenticação, seguro upload de bytes, estado persistente multiusuário, RLS/tenancy, worker durável, 9 outputs reais e gates de qualidade/recovery, sem reclamação de produção por evidência estática.
- Ref: `docs/production/RENDER_FREE_STAGING_RUNBOOK.md`. Histórico GCP/AWS W007 permanece imutável BLOCKED, PROD readiness permanece FALSE.

## Próximo ID disponível

`D-0023`


