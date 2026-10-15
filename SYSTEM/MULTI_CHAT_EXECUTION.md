# MULTI-CHAT EXECUTION — Academy Suno

**Execution mode:** `MULTI_CHAT_EXPLICIT_WORKERS`  
**Operator directive:** 2026-10-15, reactivate the original multi-chat Orchestrator → Worker workflow.  
**Decision:** `D-0024`, canonical target `STATE 0075`.  
**Repository:** `pablo-marchina/academy-suno`.

## Conversation separation — binding from STATE 0075 onward

- **This existing ChatGPT conversation is the sole Orchestrator conversation**. Its only actions are to read authoritative GitHub state, maintain the active exclusive Orchestrator lease, choose/preregister work, issue bounded dispatches, reconstruct GitHub task signals, verify CI and RESULT, integrate accepted worker PRs, and record decision/STATE/checkpoint updates.
- **Every new Worker attempt must actually run in a distinct ChatGPT conversation** started by the operator. The Orchestrator must not simulate `TASK_STARTED`, `TASK_COMPLETE`, code work or an external independent worker from this Orchestrator chat.
- The operator performs only the **chat startup / copy-paste** of a bounded Worker instruction. Orchestrator creates all GitHub issues/dispatches, selects task IDs, identifies dependencies, reads worker signals itself and integrates independently. No need to ferry RESULT content or manually describe task outcomes.
- Workers must **never** act as Orchestrator, claim/change the control lease, edit canonical `SYSTEM/STATE.md`, `SYSTEM/TASK_LEDGER.md`, `SYSTEM/WAVES/`, `SYSTEM/DECISIONS.md`, checkpoints or scorecards, merge their own PR, or deploy/change provider resources outside specifically approved scope.
- Worker work is **not a background agent** just because a GitHub Issue is READY/RUNNING. A user must start each separate ChatGPT worker conversation; no automatic cross-chat spawning/monitoring is implied. Orchestrator can reconstruct task status when next asked to check/continue; it cannot guarantee continuously scheduled observation absent an actual scheduled workflow.
- Workers sharing one LLM family are not automatically independent validators. Different chats isolate execution context but do not establish human gold, truly independent model judgments, blind calibration or production readiness.
- Existing historical PRs, RESULTs and CI evidence remain with **their original provenance**. Previously co-located Orchestrator/Worker execution cannot be relabeled retroactively as independent-chat execution. Re-assess separation when independence is required by a gate.

## Chat handoff procedure

1. Orchestrator checks `main`, `STATE`, exclusive lease branch `control/orchestrator-lease`, `SYSTEM/TASK_LEDGER.md` and exact task Issue `TASK_SIGNAL` comments; chooses only `READY` tasks without invalidated dependencies or previous `TASK_STARTED`.
2. Orchestrator publishes one **paste-ready** message per worker attempt and a link to its authoritative `SYSTEM/DISPATCH/` file. Handoffs for already prepared tasks are in `SYSTEM/WORKER_HANDOFFS/`.
3. Operator opens a **new chat** per worker (preferably inside the Suno Project so repository context/connectors are accessible), pastes the **single** instruction and sends it. Never put two distinct workers into one chat.
4. Worker reads `AGENTS.md`, `START_HERE.md`, `SYSTEM/CONSTITUTION.md`, `SYSTEM/TASK_SIGNALS.md`, exact dispatch, current STATE and canonical owner/lease rules. It verifies current main/STATE against **original immutable BASE provenance**, creates the isolated branch, and posts exactly one `TASK_STARTED` on its own Issue **before** work.
5. Worker implements only authorized task scope, persists its RESULT and bounded artifacts, opens one PR, waits for relevant final-head CI and posts **one terminal** `TASK_COMPLETE`, `TASK_BLOCKED` or `TASK_STALE`. A terminal `TASK_COMPLETE` requires persisted RESULT before comment. Never self-merge.
6. Orchestrator reads these facts directly from GitHub, audits provenance, gates, scoped files and CI, merges only eligible changes, and increments canonical STATE/checkpoint through its own PR.
7. The operator may return to **this** Orchestrator chat and say `Confira os Workers` or `Continue o Autopilot`; no worker result copy/paste is required.

## Two independent READY tasks at activation

| Chat | Task/Issue | Role | Original immutable attempt base | Required target |
|---|---|---|---|---|
| Worker Editorial | `W008-T001-A01` / #252 | Product Research + Editorial Operations + Compliance | STATE 0064, SHA `b8e22eca2affc0b9696087bca88603f8285c6940` | `SYSTEM/DISPATCH/W008-T001-A01.md` |
| Worker Infra Research | `W009-T002-A01` / #258 | Production Architect + SRE + FinOps, **research only** | STATE 0065, SHA `8c903c4fd6022eabb22da1ea0bea9901689f737b` | `SYSTEM/DISPATCH/W009-T002-A01.md` + pre-start amendments |

Both have **no TASK_STARTED** at activation and are independent, thus the user may start both chats concurrently. The immutable task base is historic by design; don't call it STALE solely because STATE advanced to 0075. Workers must check actual compatibility/current main, not reset state.

## Operator constraints remain in force

- **AI-only evaluation** under D-0019: no hiring or fabricating human evaluators/human gold; no false human comprehension claim.
- **Cost free-only** under D-0021/D-0022: dedicated `academy-suno` Neon Free project already exists (`cold-math-95888995`), Render `academy-suno` service Free already exists (`srv-db8gc2ivcj2c73aacg80`), Railway Free unavailable on connected account. No billable subscriptions, paid deployments or changes to unrelated projects.
- D-0023 defers **new login/auth/security feature implementation**, not pre-existing critical hard gates or read-only public staging restriction. No unsafe upload/public processing.
- Infrastructure Worker compares same-workload options on documented evidence and records missingness / DRG `PENDING_EVIDENCE`, not a fabricated winner. Use approved existing Render/Neon only for non-destructive, read-only observations; do not create/add resources without explicit new permission.
- Existing W007 blocked source-original GCP/AWS qualification and human-gold attempts remain immutable; successors are not automatically released. `PRODUCTION_READY=FALSE/NOT_AUTHORIZED`.

## Re-entry / continuity

`ORCH-G003-S001` is the observed active lease holder when this operational mode was activated, and is unchanged by the mode decision. Only the exclusive current holder can perform canonical integration. Re-read lease **each** time: if another chat has legitimately taken over, stop instead of force-updating.

**No task has been started merely by creation of this protocol or handoff files.** Worker execution begins only with actual separate-chat continuation and valid GitHub lifecycle evidence.
