# W005 START READINESS REVIEW

`REVIEW_SCOPE: readiness to start W005 production decision research`

`BASE_MAIN_SHA: f380887ae96aa15c4a3862155bc0ecf99092385c`

`BASE_STATE_VERSION: 0041`

`OUTCOME: READY_FOR_W005_RESEARCH | NOT_YET_READY_FOR_PHASE9_PRODUCTION_IMPLEMENTATION`

## Purpose

Verificar sistema, repositório e plano antes de iniciar a próxima rodada do Autopilot, distinguindo claramente duas perguntas:

1. a W005 está operacionalmente pronta para começar pesquisa/bakeoffs em paralelo?
2. o repositório já está autorizado a iniciar a implementação da stack de produção da Phase 9?

Resposta: **sim para (1); não ainda para (2), por desenho do DRG**.

## Checks executados

| Área | Verificação | Resultado | Observação |
|---|---|---|---|
| Canonical base | main/STATE/lease alinhados antes desta reconciliação | PASS | main `f380887...`, STATE 0041, lease G002 ativo |
| System Integrity | latest main integrity workflow | PASS | canonical validator passou no merge W005 |
| Protocol | Protocol 1.8 + D-0018 | PASS | production scope + DRG obrigatórios |
| Production Contract | `PROD-001..017` explícitos | PASS | production claim permanece gated |
| Decision Research Gate | alternativas/fontes/benchmark/decision outcomes/reversal | PASS | nenhuma material technology winner pré-selecionada |
| W005 DAG | T001..T009 + T013..T014 parallel; T010→T011→T012 gated | PASS_AFTER_REVIEW | duas lacunas materiais de research foram adicionadas antes do kick-off |
| Issues | #151..#165 relevantes persistidas | PASS | #164 T013 e #165 T014 adicionadas; #163 é PR histórico, não task |
| Dispatches | T001..T014 conforme wave, com T010–T012 gated | PASS | task/base/role/evidence/DoD/lifecycle definidos |
| Task Ledger | W005 rows e bases registradas | PASS | onze research tasks READY; T010..T012 PLANNED |
| Dispatch base drift | dispatch bases 0040/0041 vs successor canonical state | REVIEWED_NON_MATERIAL | worker deve inspect delta no `CONTINUITY_CHECK`; old state is potentially stale, not auto-valid |
| Worker start | branches/signals W005 | NOT_STARTED | condição esperada antes do kick-off |
| Entry-point docs | README truth corrente | FIXED_IN_REVIEW | W004 stale posture removida; W005 current scope exposta |
| Knowledge index | evidence/technology posture corrente | FIXED_IN_REVIEW | W004/W005 boundaries reconciliados |
| Issue template | Protocol 1.8 fields/lifecycle/DRG | FIXED_IN_REVIEW | branch convention `worker/...` e RESULT contract alinhados |
| Developer platform/toolchain research | repo/package/build/test/CI choices | ADDED_T013 | evita lock por conveniência na Phase 9 |
| Document parsing/source-grounding research | parser/document-AI/source extraction | ADDED_T014 | evita parser choice sem benchmark financeiro |
| Dependency manifest | production package/toolchain lock | INTENTIONALLY_PENDING | T013/T010/T012 devem decidir/condicionar; não é blocker da pesquisa |
| Human production calibration | independent human gold | OPEN_EXTERNAL/PLANNED | T005 define protocolo; não fabricar disponibilidade humana |
| Deadline/submission facts | external logistics | UNKNOWN_EXTERNAL | não bloqueia W005; bloqueia final global stop |

## Readiness judgment

### Ready agora

A W005 pode começar imediatamente porque:

- contrato de produção e critérios de decisão existem antes da escolha da stack;
- as **onze** pesquisas iniciais independentes agora cobrem requisitos, frontend/API, orchestration, tenancy/security/data, eval science, adaptive runtime, observability, deployment/reliability, benchmark methodology, developer platform/toolchain e document parsing/source-grounding;
- cada uma tem dispatch durável, Issue, base SHA/state, role, evidence contract e DoD;
- síntese, red-team e implementation planning estão corretamente impedidos de antecipar evidência;
- W004 permanece baseline/counterfactual em vez de ser apagado ou promovido indevidamente;
- o fluxo preserva hard gates determinísticos enquanto investiga adaptação para decisões suaves.

### Não autorizado ainda

Ainda **não** é correto criar a arquitetura final de produção ou iniciar o bulk implementation da Phase 9 escolhendo, por preferência, frontend/auth/database/parser/workflow/provider/toolchain/observability/deployment.

O gate correto é:

```text
W005-T001..T009 + T013..T014 evidence
        ↓
W005-T010 architecture synthesis
        ↓
W005-T011 independent red-team
        ↓
W005-T012 final fan-in + implementation DAG
        ↓
Phase 9 implementation waves
```

Spikes experimentais limitados dentro das tasks W005 são permitidos quando necessários para produzir benchmark/evidência; eles não viram stack de produção automaticamente.

## Gaps encontrados e disposição

### G-001 — README estava stale

O README ainda descrevia W004 como postura corrente, inclusive provider/runtime como bloqueado e fan-in antigo pendente. Isso poderia induzir workers/evaluators a trabalhar sobre truth obsoleta.

**Disposition:** corrigido nesta revisão; README passa a apontar Phase 8/W005, Production Contract, DRG e boundaries correntes.

### G-002 — Knowledge Index estava stale

O índice parava em evidências iniciais e dizia que a stack final deveria ser escolhida após W001, incompatível com D-0018.

**Disposition:** corrigido nesta revisão; registry e technology posture reconciliados com W004/W005.

### G-003 — Issue template estava stale

Template usava branch `task/...`, roles antigas e não exigia Success/Production refs, DRG nem lifecycle signals.

**Disposition:** corrigido nesta revisão.

### G-004 — Manifest/toolchain final de produção ainda não existe

Não há `pyproject.toml`/Node workspace/package lock de produção congelado. Isso seria um blocker se a Phase 9 fosse começar agora, mas **não é um defeito da Phase 8**: linguagem/package layout/frontend runtime são material choices e o DRG proíbe lock sem evidência.

A revisão detectou que a W005 original não tinha uma task dedicada a pesquisar repository/workspace/package manager/build graph/test architecture/CI/CD. Sem isso, T010 teria de inventar parte da plataforma de desenvolvimento.

**Disposition:** W005-T013 / Issue #164 adicionada. O manifest/toolchain final continua intentionally pending até a síntese T010/T012.

### G-005 — Validator não prova a existência remota de Issues/signals

`System Integrity` valida os arquivos canônicos, wave schema, checkpoints e invariantes, mas não substitui uma auditoria remota do GitHub Issues/lifecycle.

**Disposition:** nesta revisão, Issues/dispatches/ledger foram inspecionados diretamente. Não alterar `scripts/validate_system.py` casualmente porque ele integra o protocolo e qualquer mudança ali exige o procedimento de protocol change. Um hardening futuro pode automatizar cross-link local/remote se seu valor superar a complexidade.

### G-006 — dispatch base é anterior ao estado sucessor da wave

Os dispatches W005 originais foram gerados em `STATE 0040` / main `1cfeb...`; o bootstrap da própria wave avançou o canônico para 0041, e esta revisão avança para 0042. T013/T014 foram criados em 0041 / `f380...`.

A Constituição classifica resultado baseado em estado antigo como **potencialmente stale**, não automaticamente inválido. A revisão do delta confirma que os estados sucessores até esta reconciliação não alteraram Production Contract/DRG nem materialmente os objetivos dos research attempts; a única mudança de dependência material foi expandir T010 para consumir T013/T014, e T010 ainda não pode iniciar.

**Disposition:** research attempts A01 permanecem elegíveis para continuity review, mas cada worker é obrigado a executar `CONTINUITY_CHECK` contra o main observado, comparar o delta material desde sua base e emitir `TASK_STALE` se encontrar qualquer incompatibilidade. `OBSERVED_MAIN_SHA` deve registrar o head real no `TASK_STARTED`; nunca falsificar igualdade com `BASE_COMMIT_SHA`.

### G-007 — document parser/document-intelligence estava subespecificado

T004 cobria upload/storage/security, mas a wave original não tinha um bakeoff dedicado à qualidade de parsing/extraction financeira. Como números, unidades, table roles e provenance são centrais ao case, deixar essa escolha para T010 violaria a regra de systematic research para decisões materiais.

**Disposition:** W005-T014 / Issue #165 adicionada com baseline W004, corpus representativo, métricas separadas de numeric/date/entity/table-role/unit/provenance e fail-closed source trust.

## Kick-off rule

A partir do merge desta reconciliação, o início correto é abrir **W005-T001..T009 + W005-T013..T014 em paralelo**. Não é necessária uma nova fase de planejamento antes disso.

O Orchestrator deve reconstruir o lifecycle por `TASK_SIGNALS`/Issues/results, integrar micro-fan-ins válidos e manter T010 bloqueada até os onze inputs obrigatórios serem aceitos.

## Claim boundary

`READY_FOR_W005_RESEARCH` significa que o sistema está preparado para começar o programa evidence-driven que decidirá a arquitetura.

Não significa `PRODUCTION_READY`, não significa que a stack está escolhida e não significa que a Phase 9 já pode ignorar T010/T011/T012.
