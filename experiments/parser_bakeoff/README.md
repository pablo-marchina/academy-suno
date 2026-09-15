# W002-T002 parser/source-trust bakeoff

This experiment evaluates parser **behavioral guarantees**, not parser brand popularity.

## Corpus

The checked-in manifests under `data/fixtures/parser_bakeoff/` cover three real primary/public source families:

- Copom monetary-policy minutes (Banco Central do Brasil, PDF);
- issuer material disclosure / Fato Relevante (Petrobras, HTML);
- earnings/results report (Petrobras 2T26, PDF with financial tables).

The manifests contain source provenance, stable source-identity and golden-check hashes, manually checked critical anchors, required qualifiers and table-role bindings. Raw source documents are **not vendored**. This avoids stale copies and licensing ambiguity. The live runner computes raw byte SHA-256 when it can fetch the official source.

## Run

Offline/reproducible behavioral snapshot:

```bash
python experiments/parser_bakeoff/run_bakeoff.py \
  --output experiments/parser_bakeoff/results.json
```

Live replay against primary URLs:

```bash
python experiments/parser_bakeoff/run_bakeoff.py --live \
  --output experiments/parser_bakeoff/live-results.json
```

Live PDF candidates are optional `pypdf` and `pdftotext -layout`; HTML candidates use Python stdlib and a deliberately weak regex baseline.

## Trust rule

A parser does **not** pass because all numbers are present. For table-derived facts it must preserve or reconstruct row, column, unit and period/metric roles. If tokens survive but roles do not, the document is `REVIEW_REQUIRED`. If values are bound to the wrong roles, the result is `FAIL` and `silent_corruption=true`.

## Why parser lock remains conditional

This small corpus is enough to establish kill criteria and prove that flat-text success is unsafe. It is not enough to lock a vendor/library. A final parser selection must replay raw bytes across a larger development corpus, record raw source hashes, and demonstrate stable table-role provenance plus deterministic failure on ambiguous extraction.
