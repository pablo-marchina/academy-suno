# Interface guiada em português para anotação W004

Esta interface reduz a fricção operacional sem alterar o protocolo de evidência humana. Ela não sugere respostas, não auto-classifica itens e não expõe target, evaluator, provider/model identity ou material held-out.

## Como usar

Depois de inicializar a sessão normalmente, rode apenas:

    python -m app.annotation.friendly --session .annotation_work/primary_a/session.json

A interface:

- continua automaticamente do próximo item pendente;
- mostra cada pergunta em português com explicação simples das opções;
- salva o progresso após cada item;
- permite interromper com Ctrl+C e retomar depois com o mesmo comando;
- ao completar 36/36, exporta automaticamente o JSONL e o sidecar de proveniência na pasta da sessão.

Para PRIMARY_B, use a sessão independente correspondente:

    python -m app.annotation.friendly --session .annotation_work/primary_b/session.json

As regras de independência permanecem as mesmas: duas pessoas humanas diferentes, sessões separadas e nenhuma troca de labels/notas antes de ambos os exports estarem congelados.
