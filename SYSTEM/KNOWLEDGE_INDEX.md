# KNOWLEDGE INDEX

Este arquivo indexa conhecimento consolidado. Ele não substitui o `STATE`; serve para evitar inflar o estado canônico com detalhes de pesquisa.

## Camadas de informação

```text
RAW RESULTS / ISSUES
        ↓
KNOWLEDGE INDEX + artefatos
        ↓
CANONICAL STATE
```

O `STATE` deve permanecer compacto e suficiente para continuar o projeto. Detalhes extensos ficam aqui, em Issues ou em artefatos próprios.

## Evidence registry

| Evidence ID | Claim / Topic | Source / Artifact | Status | Integrated State |
|---|---|---|---|---|
| E-0001 | Briefing primário: objetivo, escopo, 3×3, evaluator, entregáveis e vídeo eliminatório | `docs/case/CASE_BRIEF_TRANSCRIPTION.md` | VERIFIED | 0008 |
| E-0002 | Suno, concorrentes, AI-finance comparables, content benchmark e unknowns internos | `docs/research/partner-competitor-ai-benchmark-2026-09-14.md` | VERIFIED | 0008 |
| E-0003 | Case Contract consolidado sem inventar pesos/deadline | `SYSTEM/CASE_CONTRACT.md` | VERIFIED | 0008 |
| E-0004 | Partner Contract com dor, contexto, hipóteses e unknowns explícitos | `SYSTEM/PARTNER_CONTRACT.md` | VERIFIED | 0008 |

Status sugeridos: `VERIFIED | PROVISIONAL | CONFLICTED | SUPERSEDED`.

## Knowledge areas

### Case brief

- fonte primária ingerida e transcrita;
- pergunta norteadora e escopo congelados no Case Contract;
- 6 entregáveis obrigatórios;
- vídeo real é hard gate eliminatório;
- conflito de duração preservado: “5 a 7” vs “máximo 5”; regra operacional <=5 registrada em A-0001;
- deadline e submissão continuam UNKNOWN.

### Partner / Users / Context

- dor primária sustentada pelo briefing: transformação de conteúdo financeiro denso sem perda de rigor e com avaliação objetiva;
- públicos externos explícitos: Iniciante, Intermediário, Avançado/Institucional;
- owner/decision maker/workflow interno Suno continuam UNKNOWN;
- valor operacional de tempo/retrabalho/reuso é hipótese, não fato.

### Competitors / Benchmarks

- Empiricus: acessibilidade/didática;
- Nord: segmentação por jornada/tier;
- XP: cadência e reutilização multicanal;
- BTG: benchmark de linguagem avançada/institucional;
- comparáveis globais reforçam source lineage, first-party data e trust layer.

Detalhes: `docs/research/partner-competitor-ai-benchmark-2026-09-14.md`.

### Product / Technology

Hipótese candidata, ainda não decisão: content transformation + trust layer com factual backbone, fan-out 3×3, Hybrid Evaluator e targeted repair. Stack final deve ser escolhida após W001.

### Evaluation / Experiments

Prioridades:
- readability PT-BR;
- ontology/domain term calibration;
- claim/anchor grounding;
- golden + held-out dataset;
- confusion matrix dos níveis;
- format-specific evals;
- retry/cost/latency telemetry;
- baseline contra prompt-only/manual simplificado.

### Economics / Metrics

Ainda não há ROI interno Suno. O briefing exige custo/latência no relatório; proxies de eficiência operacional serão tratados como hipóteses até evidência.

### Strategy

Diferenciação candidata: não “usar agentes”, mas provar que a transformação editorial detecta quando está errada, explica a falha, preserva source lineage e corrige com métricas reproduzíveis.

## Regra

Evidência candidata produzida por worker só recebe um `Evidence ID` definitivo quando aceita pelo Orchestrator durante integração.
