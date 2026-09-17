# W004 parser/source-trust generalization bakeoff

This task extends the W002 source-trust contract without selecting a parser vendor. The goal is to distinguish **safe extraction behaviour** from attractive-but-unsafe value coverage.

## Corpus

The fixtures are manually curated from current primary sources and live under `experiments/parser_w004/fixtures/` so this worker stays inside its ownership paths.

| Family | Primary evidence | Structural risk exercised |
|---|---|---|
| Copom | BCB, Ata da 279ª reunião (17 Jun 2026) | same table, different projection columns/period roles |
| CVM ITR | CVM 2026 ITR open-data resource + CVM/SEP schema notice effective 29 Aug 2026 | mandatory field identity/schema drift; identical `required` values bound to different field roles |
| Earnings/results | Petrobras, Relatório de Desempenho 1T26 | row-role swap plus cross-table BRL-million vs USD-million unit confusion |

Official source URLs are stored in each fixture. Petrobras Table 1 and Table 3 were visually checked from the issuer PDF. Raw response bytes were not available in the execution environment, so `raw_bytes_sha256` is `null` rather than fabricated.

## Trust contract

For every critical table-derived anchor, `table_id`, `row_key`, `row_role`, `column_key`, `column_role`, `unit`, and `period_role` are part of the fact. The scorer applies these non-compensating gates:

- missing or altered critical value -> `FAIL`;
- explicit wrong table/row/column/unit/period provenance -> `FAIL`;
- exact values with missing provenance -> `REVIEW_REQUIRED`, never `PASS`;
- 100% numeric/value coverage does **not** compensate for wrong roles.

`silent_corruption=true` is emitted whenever all golden values survive but the extraction is still non-PASS because semantics/provenance were lost or corrupted.

## Behaviour probes

`provenance_preserving_reference` is the gold structural reference. `flat_value_only` models extraction that retains values while dropping table semantics. `wrong_role_probe` keeps values intact while binding one value to the wrong row/period role in each family. `wrong_unit_probe` specifically crosses Petrobras Table 1 (`R$ milhões`) with Table 3 (`US$ milhões`).

These probes are **not vendor/library candidates**. They test the acceptance contract. Therefore the implementation decision intentionally remains `UNLOCKED`: this attempt does not compare multiple viable parser libraries on identical raw bytes.

## Reproduce

```bash
python3 experiments/parser_w004/run_bakeoff.py --output /tmp/parser_w004_results.json
python3 -m unittest discover -s tests/parser_w004 -p 'test_*.py' -v
```

Expected aggregate behaviour:

- provenance-preserving reference -> `PASS`;
- flat values -> `REVIEW_REQUIRED` with full value coverage;
- wrong role -> `FAIL` with full value coverage;
- wrong unit/table -> `FAIL` on the earnings fixture;
- parser implementation identity -> `UNLOCKED`.

## Limitations / next evidence

This experiment materially broadens document/layout/role failure coverage, but it does not establish a production parser winner. A lock would require replaying the **same raw bytes** through at least two viable parser stacks and measuring role-preservation/error rates, determinism, warnings, latency and fallback behaviour. OCR/scanned PDFs also remain outside this attempt.
