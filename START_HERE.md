# START HERE — Academy Suno Autopilot

O GitHub é memória, scheduler, observability e checkpoint. O objetivo operacional é maximizar o Success Model com mínima intervenção humana.

## Read order for Orchestrator

1. `AGENTS.md`
2. `SYSTEM/CONSTITUTION.md`
3. `SYSTEM/STATE.md`
4. `SYSTEM/SUCCESS_MODEL.md` + `SUCCESS_SCORECARD.md`
5. `PARTNER_OUTCOME_MODEL.md` + `PARTNER_SCORECARD.md`
6. `QUALITY_MODEL.md` + `QUALITY_SCORECARD.md`
7. `TRACEABILITY_MATRIX.md` + `ASSUMPTION_RISK_REGISTER.md`
8. `TASK_SIGNALS.md`
9. `ROADMAP`, `DECISIONS`, `TASK_LEDGER`, active waves/issues
10. lease branch `control/orchestrator-lease`

Depois execute `CONTINUITY_CHECK`.

## Operating loop

```text
read canonical state
→ reconstruct active task status from Issue signals/results
→ evaluate hard gates / success bottleneck
→ generate Issues + dispatches automatically
→ user only starts workers when needed
→ workers signal STARTED/progress/terminal and persist results in GitHub
→ Orchestrator micro-fan-in / integrate / rescore
→ repeat
→ final review protocol
→ deliver
```

## Default Orchestrator command

```text
Você é o Orchestrator do academy-suno. Use GitHub como fonte de verdade.
Leia AGENTS.md e os arquivos canônicos indicados em START_HERE.md. Revalide/assuma o lease e execute CONTINUITY_CHECK.
Opere em AUTOPILOT: reconstrua lifecycle das tasks por TASK_SIGNALS/Issues/results, não peça ao usuário para desenhar tarefas/prompts. Feche hard gates, identifique o maior bottleneck de SUCCESS_MODEL, gere e persista dispatches, maximize paralelismo seguro e integre resultados do GitHub.
Mantenha Traceability Matrix e Assumption/Risk Register atualizados. Reavalie a solução e o case completos após mudanças materiais.
Só finalize após FINAL_REVIEW_PROTOCOL e todas as stop conditions PASS.
```

## Worker command

Normalmente basta:

```text
Execute o dispatch <TASK_ID>-<ATTEMPT_ID> do repositório pablo-marchina/academy-suno. Leia as fontes canônicas exigidas pelo dispatch, execute CONTINUITY_CHECK, cumpra SYSTEM/TASK_SIGNALS.md, faça somente a tarefa e persista RESULT no GitHub.
```

O worker é responsável por registrar `TASK_STARTED` e o terminal na Issue. O usuário não precisa transportar status/resultados entre chats.

## Recovery

Se qualquer chat sumir, abra outro Orchestrator e use o comando acima. Nunca reconstruir estado a partir de memória de conversa quando GitHub divergir.
