# Grounding semantic ablation

`W003-T002` deliberately does **not** select a semantic/NLI/LLM backend. The reusable
`run_semantic_ablation()` harness compares the same claims and hard-gate inputs with
the semantic adapter disabled vs enabled. A candidate backend only earns adoption if
measured incremental detection/uncertainty value exists on development gold; source,
deterministic factual and policy hard-gate outcomes must remain invariant.

The automated grounding tests exercise the harness with deterministic stubs, including
an adversarial always-SUPPORTED adapter proving that a semantic sensor cannot convert a
known deterministic/source/policy hard failure into PASS.
