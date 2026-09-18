# Demo Storyboard / Script — target 4:40, hard cap 5:00

**Goal:** prove the system mechanics and evidence discipline live without overstating human/provider/production evidence.

**Hard rule:** stop at 5:00 even if a section slips. The target timeline is 4:40, leaving 20 seconds of operational margin.

## Pre-demo setup

Run once from a clean checkout:

```bash
python scripts/release_smoke/run_release_smoke.py \
  --workdir /tmp/academy-suno-release-smoke \
  --output /tmp/academy-suno-release-smoke/manifest.json
```

Have these visible before recording:

- terminal at repository root;
- `/tmp/academy-suno-release-smoke/manifest.json`;
- `/tmp/academy-suno-release-smoke/proof/proof_report_v001.json`;
- `/tmp/academy-suno-release-smoke/evidence-cockpit.html` open in a browser;
- `docs/release/EVIDENCE_PACKET.md`.

Do not preload any fake human/provider artifact.

## 0:00–0:25 — Problem and contract

**Screen:** README architecture + evidence posture.

**Say:** “A mesma fonte precisa virar nove combinações de público e formato sem perder factualidade, proveniência ou rastreabilidade. O ponto central aqui não é mostrar uma caixa verde: é mostrar o que foi provado, o que é apenas diagnóstico e o que ainda está bloqueado.”

**Show:** `PROVEN`, `DIAGNOSTIC_ONLY`, `PRODUCTION_UNKNOWN`, `BLOCKED`, `PENDING`.

## 0:25–1:05 — Real code path

**Screen:** `experiments/w003_e2e/run_proof.py`, then `app/evidence_cockpit.py`.

**Say:** “O proof executável cria exatamente 3 públicos × 3 formatos, passa pelos hard gates, persiste estado no RunStore, separa retry de repair e reabre o estado antes de finalizar. O cockpit não cria outra verdade: só projeta os artefatos persistidos.”

**Show in code:** `REPAIR_JOB_ID = "beginner:carousel"`, `transport_retry_limit=1`, `max_quality_repairs=1`, and the cockpit inputs for runstore/proof/telemetry.

## 1:05–1:55 — Persisted FAIL → repair → PASS

**Screen:** `proof_report_v001.json`, section `repair_lineage`.

Use a terminal if helpful:

```bash
python -m json.tool /tmp/academy-suno-release-smoke/proof/proof_report_v001.json
```

**Say:** “Aqui não é uma animação: a tentativa começa com status FAIL por valor factual incorreto. A repair é branch-local, muda o hash da saída, roda novamente os hard gates e termina PASS. Os hashes before/after e os failure codes ficam persistidos.”

**Show:** `before_snapshot_serialized.status = FAIL`; `after_snapshot.status = PASS`; different `before_output_hash` / `after_output_hash`; `fresh_hard_gate_runs = true`; `siblings_immutable = true`.

## 1:55–2:50 — Evidence cockpit with provenance

**Screen:** live `evidence-cockpit.html`.

**Say:** “A interface mantém o 3×3, a linhagem de repair, telemetria e provenance. Um FAIL não é compensado por um indicador bonito. Missing evidence continua N/A/unknown.”

**Show:** repair panel; source/run/job/attempt fields; evidence scope `MECHANICS_ONLY`; evidence classes.

**Say explicitly:** “MECHANICS_ONLY não significa qualidade do provider nem readiness de produção.”

## 2:50–3:35 — Parser/source-trust guard

**Screen:** release-smoke manifest and/or `experiments/parser_w004/observed_results.json`.

**Say:** “Também testamos um risco silencioso: manter o número certo com a linha, coluna, unidade ou período errado. O reference preservando provenance passa; flat values vira REVIEW_REQUIRED; wrong-role fica FAIL mesmo com 100% de value coverage.”

**Show:** parser implementation decision remains `UNLOCKED`.

## 3:35–4:15 — What is still unknown

**Screen:** `docs/release/EVIDENCE_PACKET.md`.

**Say:** “Agora a parte mais importante para não vender além da evidência: thresholds de audiência seguem DIAGNOSTIC_ONLY porque ainda faltam duas anotações humanas independentes. As confusion matrices estão PENDING/BLOCKED. Qualidade, latency, usage e cost de provider real seguem PRODUCTION_UNKNOWN/BLOCKED. O backend semântico e o release final também continuam pendentes dos seus experimentos.”

Do not show synthetic pricing as economics.

## 4:15–4:40 — Close with release boundary

**Screen:** final review checklist.

**Say:** “O que está pronto hoje é uma base reproduzível, auditável e demonstrável com unknowns explícitos. O pacote final só pode promover release readiness depois do fan-in W004-T008 com human gold, provider observado, ablation e clean E2E. Até lá, readiness continua PENDING.”

**End by 4:40.**

## Overrun cuts

If the demo is running late, cut in this order:

1. reduce parser explanation to one sentence (save ~15s);
2. skip code scrolling and point directly to constants/arguments (save ~15s);
3. shorten closing to: “T011 prova reprodutibilidade; T008 decide release depois dos blockers externos.” (save ~10s).

Never cut the persisted FAIL→repair→PASS proof or the explicit unknown/blocker section.
