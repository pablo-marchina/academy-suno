# W006-T006-A01 — authenticated live-cockpit frontend bakeoff

`TASK_ID: W006-T006`  
`ATTEMPT_ID: A01`  
`CONTRACT_VERSION: 1.0.0`  
`STATUS: EVIDENCE_GATED_NO_WINNER`

## Scope

This slice evaluates two framework-neutral frontend/editor shells over the accepted W006-T001-A02 production contract:

1. `server_hypermedia_shell` — server-oriented rendering/partial-update shape.
2. `client_event_shell` — client event-projection shape.

They intentionally share the same `LiveCockpitProjector`, canonical `CommandEnvelope` builder and durable view model. This evidence does **not** select React/Next.js/HTMX/another framework or package manager; a concrete framework remains Decision Research/evidence gated.

## Same-slice path

Both candidates expose the same product sequence:

`authorized workspace → upload/source → live run → 3×3 cells → citations → evaluation/repair → reconnect(snapshot + replay)`

The upload control is transport-neutral but maps to the production `CommandEnvelope`; live updates consume the accepted `EventEnvelope`. The server supplies an `AuthorizedStream`. An opaque replay cursor may select replay position on the server, but the client projector never derives tenant/resource identity from it.

## Security and state invariants

- Authorization scope is server supplied as `org_id + workspace_id + run_id` and is checked before source/event/trace projection.
- Nested protected source, cell, citation, evaluation, repair and trace records are scope checked independently; a matching outer event cannot smuggle a foreign inner record.
- At-least-once duplicate delivery is deduplicated by stable `event_id`.
- Stream `event_revision` must advance; resource `result_revision` cannot regress the last observed revision for that resource.
- The static W004 recipient path is not imported and is not a fallback. Missing authoritative source/snapshot state fails closed.
- `FAIL` and `REVIEW_REQUIRED` remain first-class visible cell states; no green aggregate/readiness score is synthesized.
- Candidate UI state is rendered only from the durable snapshot plus accepted authoritative events.

## Accessibility / dynamic update evidence

Both shells render:

- a labeled workspace context;
- labeled file upload control and help text;
- semantic section headings;
- a 3×3 output collection with explicit text status (not color-only status);
- `role="status" aria-live="polite"` for run/revision updates;
- cell headings bound through `aria-labelledby`.

The executable assertions live in `tests/cockpit/test_live_cockpit.py` and cover both candidate renderers.

## Cross-tenant adversarial evidence

The test suite attempts three protected projections using a foreign scope:

| Vector | Foreign value | Expected result |
| --- | --- | --- |
| source in snapshot | `workspace_id` | reject before projection |
| trace in snapshot | `org_id` | reject before projection |
| authoritative event | `workspace_id` | reject before event application |

A fourth test supplies a correctly scoped outer event with a foreign nested cell payload and requires fail-closed behavior. Acceptance metric is exact: successful cross-tenant source/event/trace projections = `0`.

## Reconnect / replay evidence

`reconnect()` always reconstructs state from a server-authorized durable snapshot and then applies canonical events newer than the snapshot stream revision. Replay position is not exposed in the view model and is not accepted as an authorization input. Duplicate event IDs are harmless no-ops; stale stream revisions fail closed.

## Candidate decision posture

No framework winner is declared by this task. The bakeoff deliberately separates the invariant product/state/security layer from the rendering shell so future DRG work can compare implementation complexity, interaction ergonomics, deployment/runtime fit, accessibility tooling and measured production behavior without changing authorization or replay semantics.
