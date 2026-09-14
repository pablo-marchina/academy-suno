# ORCHESTRATOR LEASE PROTOCOL

O objetivo deste protocolo é garantir que apenas um chat Orchestrator tenha autoridade de integração canônica por vez.

## Localização dinâmica

O estado do lease **não vive no `main`**. Ele vive em:

- branch: `control/orchestrator-lease`
- path: `SYSTEM/ORCHESTRATOR_LEASE.json`

A branch de controle existe para permitir claim/release rápido sem criar PR para cada rotação.

## Estrutura

```json
{
  "schema_version": 1,
  "generation": 1,
  "lease_id": "ORCH-G001",
  "holder_session_id": "ORCH-G001-S001",
  "status": "ACTIVE",
  "base_state_version": "0004",
  "base_main_commit_sha": "<40 hex>",
  "handoff_to": null,
  "note": "..."
}
```

`status`: `AVAILABLE | ACTIVE | HANDOFF_READY`.

## Claim atômico

1. Resolva o SHA atual do `main` e o `STATE_VERSION`.
2. Leia o lease na branch de controle e guarde o blob SHA retornado pelo GitHub.
3. Se `AVAILABLE`, escolha um `holder_session_id` único para a geração e atualize o JSON usando o blob SHA observado.
4. Se `HANDOFF_READY`, somente o destino indicado em `handoff_to` deve assumir; incremente `generation` e gere novo `lease_id`.
5. Se o update falhar por conflito de SHA, outro Orchestrator atualizou primeiro. Recarregue; não force.
6. Execute `CONTINUITY_CHECK` depois do claim.

## Antes de integrar

Imediatamente antes de criar/atualizar uma integração canônica:

- releia o lease;
- confirme `status=ACTIVE`;
- confirme `holder_session_id` igual ao seu;
- confirme que o `STATE_VERSION` esperado continua atual;
- resolva novamente o SHA do `main`.

Se qualquer condição falhar: `LEASE_LOST` e abortar integração.

## Handoff

O Orchestrator atual atualiza o lease para:

```json
{
  "status": "HANDOFF_READY",
  "handoff_to": "<session-id planejado>"
}
```

O sucessor lê o SHA do blob, valida o handoff e executa update atômico para a próxima geração, com `status=ACTIVE`.

## Recovery de Orchestrator abandonado

Como chats não têm heartbeat confiável, não existe TTL automático. Se o holder desapareceu, o operador humano pode autorizar takeover. O novo Orchestrator deve:

1. registrar no campo `note` que é `MANUAL_TAKEOVER`;
2. incrementar a geração;
3. usar update com o blob SHA observado;
4. executar auditoria/continuity check antes de qualquer integração.

Nunca sobrescreva o lease com force update baseado em conteúdo antigo.
