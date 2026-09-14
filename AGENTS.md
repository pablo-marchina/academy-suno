# AGENTS.md — Academy Suno

Estas instruções valem para qualquer chat/agente que trabalhe neste repositório.

## Regra zero

O histórico de uma conversa **não é a fonte de verdade**. A fonte de verdade é o repositório, nesta ordem:

1. `SYSTEM/CONSTITUTION.md` — protocolo e regras de operação.
2. `SYSTEM/STATE.md` — estado canônico atual do projeto.
3. `SYSTEM/PARTNER_OUTCOME_MODEL.md` — verdade operacional sobre a dor e valor para o parceiro.
4. `SYSTEM/PARTNER_SCORECARD.md` — avaliação corrente de impacto/utilidade para o parceiro.
5. `SYSTEM/QUALITY_MODEL.md` — qualidade global do case e aderência à avaliação.
6. `SYSTEM/QUALITY_SCORECARD.md` — avaliação corrente do case.
7. `SYSTEM/ROADMAP.md`, `SYSTEM/DECISIONS.md`, `SYSTEM/TASK_LEDGER.md`.
8. `SYSTEM/WAVES/W###.json` — manifests executáveis.
9. GitHub Issues/PRs — fila operacional e resultados ainda não integrados.

## Objetivo dominante

A prioridade do sistema é, nesta ordem:

1. **maximizar o valor real esperado para o parceiro resolvendo a dor correta**;
2. cumprir integralmente objetivo, entregáveis, restrições e critérios do case;
3. tornar a recomendação rigorosa, defensável, clara e acionável;
4. usar velocidade/paralelismo para reduzir o tempo até esse resultado.

Uma solução que recebe boa avaliação mas ajuda menos o parceiro do que uma alternativa viável é subótima e deve ser reaberta.

## Bootstrap obrigatório

Antes de trabalhar, leia as fontes aplicáveis, identifique `PROTOCOL_VERSION`, `STATE_VERSION`, SHA do `main`, papel, `TASK_ID` e `ATTEMPT_ID`, e execute `CONTINUITY_CHECK`.

Se qualquer referência divergir, marque `STALE_INPUT`.

## Autoridade e lease

- Existe no máximo um Orchestrator com autoridade de integração por vez.
- O lease dinâmico vive na branch `control/orchestrator-lease`, arquivo `SYSTEM/ORCHESTRATOR_LEASE.json`.
- Claim/handoff usa compare-and-swap pelo blob SHA observado.
- Antes de integração canônica o Orchestrator deve reler e validar o lease.
- Workers nunca alteram arquivos canônicos.

## Partner-first

Antes de recomendar solução, o sistema precisa construir um `PARTNER_CONTRACT` suficientemente evidenciado: quem sente a dor, qual problema real, frequência/severidade, causa raiz, impacto, comportamento atual, workaround/status quo, resultado desejado, restrições e barreiras de adoção.

Toda solução deve mostrar explicitamente:

- qual dor prioritária resolve;
- por que essa dor é mais importante que alternativas;
- mecanismo causal de geração de valor;
- benefício esperado e como medi-lo;
- por que é melhor que status quo/alternativas relevantes;
- viabilidade de implementação;
- caminho de adoção, owner e primeiro passo/piloto;
- riscos, trade-offs e condições em que a solução não deve ser escolhida.

## Proveniência obrigatória

Toda tentativa declara `TASK_ID`, `ATTEMPT_ID`, `BASE_STATE_VERSION`, `BASE_COMMIT_SHA`, dependências, papel, objetivo, definição de pronto e formato de saída. `TASK_ID + ATTEMPT_ID` nunca é reutilizado.

## Paralelismo

Tarefas independentes devem ser paralelizadas. Workers usam branches isoladas por tentativa quando alteram arquivos. O Orchestrator libera dependentes assim que as dependências fecham; não espera barreiras artificiais de wave.

## Entrega de worker

Toda entrega deve terminar com `RESULT` contendo identidade/proveniência, status, confiança, findings, evidências, impacto no parceiro, delta proposto, riscos, artefatos e próximos passos. Resultado relevante deve existir no GitHub, nunca exclusivamente no chat.

## Checkpoints e recuperação

Todo incremento de `STATE_VERSION` exige snapshot idêntico em `SYSTEM/CHECKPOINTS/STATE-v####.md`. Checkpoints antigos são append-only.

## Segurança contra drift

Decisão `LOCKED` só muda por `DECISION_REVIEW` explícita.

## Regra de supremacia

Nenhuma tarefa, feature, análise ou elemento de apresentação deve permanecer apenas porque é sofisticado. Se não aumentar valor esperado para o parceiro, cumprir requisito obrigatório ou reduzir risco material, deve sair do caminho crítico.
