# AUTOPILOT — Quality Optimization Loop

## Objetivo

Minimizar intervenção humana enquanto o sistema itera até o melhor case defensável possível segundo `SYSTEM/QUALITY_MODEL.md`.

## Responsabilidade do Orchestrator

O Orchestrator deve, sem depender do usuário para desenhar prompts:

1. ler estado, Quality Model e Quality Scorecard;
2. identificar o maior gap de qualidade ou hard gate bloqueado;
3. decompor o gap em tarefas paralelizáveis;
4. criar Issues/manifests e gerar o prompt completo de cada worker;
5. persistir cada prompt em `SYSTEM/DISPATCH/<TASK_ID>-<ATTEMPT_ID>.md` quando a tarefa for liberada;
6. receber resultados pelo GitHub;
7. executar staleness/provenance check;
8. sintetizar e integrar o que melhorar o case;
9. rodar avaliação completa, Red Team e scorecard novamente;
10. repetir até `STOP_CONDITION: PASS`.

## Intervenção humana permitida/necessária

O usuário não deve precisar decidir quais agentes criar, escrever prompts, transportar resultados ou escolher o próximo ciclo.

Intervenção humana é reservada para:

- fornecer briefing/arquivos inacessíveis;
- decisões de negócio genuinamente subjetivas que o case deixa ao candidato;
- permissões/logins/ações administrativas;
- iniciar um novo chat worker quando o produto ChatGPT não puder spawná-lo automaticamente;
- resolver `HUMAN_DECISION_REQUIRED`.

Quando for necessário abrir worker manualmente, o Orchestrator deve entregar um dispatch autocontido. O usuário idealmente envia apenas algo como: `Execute o dispatch W003-T004-A01 do repositório academy-suno.`

## Loop obrigatório

```text
INGEST / CASE CONTRACT
→ BASELINE
→ SCORE
→ IDENTIFY HIGHEST-VALUE GAPS
→ GENERATE DISPATCHES
→ PARALLEL EXECUTION
→ SYNTHESIS
→ RED TEAM
→ RE-SCORE FULL CASE
→ CONTINUE OR STOP
```

Nunca parar apenas porque todos os tasks de uma wave terminaram. Wave completa é evento operacional; qualidade suficiente é condição de término.

## Dispatch

Todo dispatch deve conter:

- identidade/proveniência da tentativa;
- papel;
- objetivo específico;
- relação explícita com critério/gap do Quality Scorecard;
- contexto mínimo e fontes canônicas a ler;
- dependências;
- escopo IN/OUT;
- definition of done;
- evidências requeridas;
- formato de RESULT;
- local de persistência;
- instrução para não alterar arquivos canônicos.

## Seleção de workers

O Orchestrator cria papéis dinamicamente conforme o gap. Exemplos: Market Researcher, Financial Analyst, Customer Analyst, Strategy Challenger, Fact Checker, CFO Red Team, Executive Evaluator, Storytelling Critic.

Papéis são meios; não existe obrigação de usar todos em todos os ciclos.

## Finalização

Antes de declarar `PROJECT_STATUS: COMPLETE`, o Orchestrator precisa demonstrar no Quality Scorecard que os hard gates passaram e a stop condition do Quality Model foi atingida.
