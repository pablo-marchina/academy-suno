# W004 automated blind model validation — A03

- Records: **36**
- Validator: **MODEL_AUTOMATED** via `openai/gpt-oss-120b` on Groq
- Blind input target/evaluator/model fields absent: **PASS**
- Human-gold eligible: **NO**
- Satisfies W004-T005 human gate: **NO**
- Output SHA-256: `adae7376415cd7052b8b2b84002ce0a7a5890047cb86e98dbe456747c7fe1bb4`
- Aggregate usage: `{'input_tokens': 29810, 'output_tokens': 22425, 'total_tokens': 52235}`
- Derived provider cost: `0.0179265 USD`

## Audience labels

- ADVANCED: **2**
- BEGINNER: **6**
- INTERMEDIATE: **28**
- UNSCORABLE: **0**

## Non-compensatory checks

- FACTUAL_CRITICAL_PRESERVATION: `{'FAIL': 3, 'PASS': 33, 'REVIEW_REQUIRED': 0}`
- MATERIAL_CONCEPT_PRESERVATION: `{'FAIL': 3, 'PASS': 33, 'REVIEW_REQUIRED': 0}`
- FORMAT_NATIVE_CONTRACT: `{'FAIL': 0, 'NOT_APPLICABLE': 0, 'PASS': 36, 'REVIEW_REQUIRED': 0}`

## Evidence boundary

This is a complete 36-item automated validation pass over the frozen blind bank. It is deliberately stored outside the human annotation streams and must never be relabeled as PRIMARY_A, PRIMARY_B, adjudication, or human gold.

## Attempt / rate-limit posture

- A01: failed cleanly on provider HTTP 429; no accepted artifact.
- A02: failed before network use on wrapper import; no accepted artifact.
- A03: 70s inter-batch throttle; HTTP retries: 0.
