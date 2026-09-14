# Durable Results

Resultados não podem existir exclusivamente dentro de chats.

Persistência mínima aceita:

1. comentário na GitHub Issue da tarefa; ou
2. Pull Request/commit da branch da tentativa; ou
3. artefato em caminho próprio referenciado pela Issue/manifest.

Para resultados que precisem ser congelados no repositório, use:

`SYSTEM/RESULTS/<TASK_ID>/<ATTEMPT_ID>.md`

O Orchestrator registra o `accepted_result_ref` no manifest da wave quando uma tentativa é aceita. Não apague tentativas antigas; marque-as como stale/rejected no ledger/manifest quando aplicável.
