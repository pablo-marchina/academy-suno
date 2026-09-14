# AUTOPILOT — Partner Value + Quality Optimization Loop

## Objetivo

Minimizar intervenção humana enquanto o sistema itera até a solução que mais ajuda o parceiro e o melhor case defensável para comunicá-la.

## Responsabilidade do Orchestrator

Sem depender do usuário para desenhar prompts:

1. ler estado, Partner Outcome Model/Scorecard e Quality Model/Scorecard;
2. identificar primeiro o maior gap de Partner Value/hard gate; depois gaps de qualidade do case;
3. decompor em tarefas paralelizáveis;
4. criar Issues/manifests e dispatches completos;
5. persistir prompts em `SYSTEM/DISPATCH/<TASK_ID>-<ATTEMPT_ID>.md`;
6. receber resultados pelo GitHub;
7. validar provenance/staleness;
8. integrar apenas o que aumenta Partner Value, cumpre requisito ou reduz risco material;
9. rodar Partner Jury, Red Team e avaliação completa novamente;
10. repetir até ambas stop conditions PASS.

## Intervenção humana

Reservada a materiais inacessíveis, permissões/admin, decisões realmente subjetivas/externas, abrir worker quando ChatGPT não puder spawnar e `HUMAN_DECISION_REQUIRED`.

## Loop obrigatório

```text
INGEST
→ CASE CONTRACT + PARTNER CONTRACT
→ PAIN / ROOT CAUSE / STATUS QUO
→ SOLUTION ALTERNATIVES
→ PARTNER VALUE BASELINE
→ HIGHEST-VALUE GAPS
→ GENERATE DISPATCHES
→ PARALLEL EXECUTION
→ SYNTHESIS / BUILD
→ PARTNER JURY + RED TEAM + EVALUATOR
→ RE-SCORE PARTNER + CASE
→ CONTINUE OR STOP
```

## Dispatch

Todo dispatch deve conter identidade/proveniência, papel, objetivo, vínculo explícito com pain/gap/hard gate, contexto, dependências, escopo, definition of done, evidências, formato de result e persistência.

## Seleção dinâmica de workers

Papéis possíveis incluem Problem Investigator, Partner Advocate, End User Judge, Economic Buyer, Implementation Owner, Counterfactual Skeptic, Market/Customer Researcher, Financial Analyst, Strategy Challenger, Fact Checker, Executive Evaluator e Storytelling Critic.

## Kill rule

Se uma linha de solução não demonstrar ligação defensável com a dor prioritária ou for dominada por alternativa mais simples/útil/viável, o Orchestrator deve despriorizá-la ou descartá-la, mesmo que seja visualmente impressionante.

## Finalização

Antes de `PROJECT_STATUS: COMPLETE`, demonstrar `PARTNER_STATUS: PASS`, `PARTNER_STOP_CONDITION: PASS`, `QUALITY_STATUS: PASS` e `STOP_CONDITION: PASS`.
