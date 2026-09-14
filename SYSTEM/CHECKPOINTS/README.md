# State Checkpoints

Este diretório contém snapshots imutáveis do estado canônico.

Regras:

1. Toda mudança de `STATE_VERSION` cria `STATE-v####.md`.
2. O checkpoint novo deve ser idêntico a `SYSTEM/STATE.md` no mesmo commit.
3. Checkpoints antigos são append-only e não devem ser editados.
4. O maior número de checkpoint no `main` deve corresponder ao `STATE_VERSION` corrente.
5. Em recovery, prefira o último checkpoint do `main`; histórico de chats não é necessário.
