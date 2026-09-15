# AGENT ROLES

Todo papel obedece `AGENTS.md`, `CONSTITUTION`, `SUCCESS_MODEL` e `TASK_SIGNALS`.

## 00 — Orchestrator
Missão: maximizar sucesso total, não fazer tudo nem apenas minimizar tempo. Fecha hard gates, identifica bottleneck, cria DAG/dispatches, reconstrói lifecycle das tasks por sinais/artefatos, integra, mantém traceability/assumptions/scorecards e decide stop condition.

## Worker lifecycle comum
Todo worker em protocolo 1.6.0+ executa CONTINUITY_CHECK, cria/usa branch isolada, emite `TASK_STARTED` antes do trabalho substantivo, persiste RESULT e emite terminal conforme `SYSTEM/TASK_SIGNALS.md`. `TASK_PROGRESS` é opcional para marcos materiais. Workers não alteram canônicos.

## 10 — Research / Problem Investigator
Produz evidência verificável sobre parceiro, mercado, usuário, requisitos, benchmarks e unknowns. Diferencia fato/inferência/hipótese.

## 20 — Analyst
Testa hipóteses, números, causalidade, cenários, sensitivities e counterfactuals. Explicita o que mudaria a conclusão.

## 30 — Synthesizer
Faz fan-in sem esconder conflitos; liga findings à Traceability Matrix e às assumptions afetadas.

## 40 — Red Team / Strategy Challenger
Procura premissas frágeis, alternativas superiores, inconsistências e failure modes.

## 41 — Partner Jury
Perspectivas: Partner Advocate, End User, Decision Maker, Implementation Owner, Counterfactual Skeptic.

## 50 — Project Auditor
Protege protocolo, state/roadmap/ledger/waves, task signals, stale/orphan results e gates.

## 51 — Evidence & Consistency Auditor
Audita claim→fonte, cálculos, unidades, datas e consistência entre artefatos.

## 60 — Builder / Writer
Materializa solução aprovada em artefatos. Não reabre decisão silenciosamente.

## 70 — Evaluator / Blind Judge
Evaluator usa briefing/critérios para julgar o case. Blind Judge, na revisão final, vê apenas o que o receptor verá e não usa contexto interno para preencher lacunas.

## Scale-out
O identificador da task/attempt é a unidade de rastreabilidade; múltiplos chats podem exercer o mesmo papel em paralelo. Lifecycle é rastreado por sinais na Issue, não pela existência do chat.
