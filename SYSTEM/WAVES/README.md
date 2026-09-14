# Wave Manifests

Cada wave executável é descrita por `W###.json` e funciona como DAG/ready queue.

Regras:

- `wave_id` deve corresponder ao nome do arquivo.
- `base_state_version` usa quatro dígitos.
- `base_commit_sha` usa o SHA completo do `main` no momento de criação da wave.
- cada task possui `task_id`, `attempt_id`, `role`, `status`, `required`, `dependencies`, `issue` e `branch`.
- `status`: `PLANNED | READY | RUNNING | BLOCKED | RESULT_RECEIVED | INTEGRATED | CANCELLED | STALE`.
- dependências não podem formar ciclos.
- novas tentativas incrementam `attempt_id`; não sobrescrevem tentativa anterior silenciosamente.
- tasks `READY` podem ser disparadas imediatamente em paralelo.
- dependentes podem ser liberados assim que todas as dependências necessárias estiverem integradas/aceitas; não é preciso esperar a wave inteira.
