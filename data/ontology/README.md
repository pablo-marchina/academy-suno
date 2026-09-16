# Finance PT-BR ontology

`finance_ptbr_v001.json` is the first versioned seed glossary for B07. The unit of evaluation is a **normalized financial concept**, not a surface string.

Design rules:

- aliases collapse only when the relation is explicit; `near_equivalent` is not treated as unquestioned semantic identity outside the configured match rule;
- contextual match rules are available on aliases to reduce false positives;
- each concept carries an initial difficulty prior and a policy per audience;
- difficulty is a feature prior, **not** a calibrated audience threshold;
- source references are governance metadata for later review/expansion, not a claim that this seed is exhaustive;
- new concepts and alias-equivalence changes require version bumps and regression fixtures.

The seed intentionally stays small enough to audit. Expansion should be driven by the gold corpus and by observed unmatched domain concepts rather than by indiscriminate glossary import.
