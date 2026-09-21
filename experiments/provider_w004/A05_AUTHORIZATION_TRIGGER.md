# W004-T004-A05 authorized Groq diagnostic and execution trigger

A04 established that the supplied secret is a Groq `gsk_` credential and that a request to `openai/gpt-oss-20b` reached Groq but returned HTTP 403. A05 is authorized to perform one read-only authenticated `GET https://api.groq.com/openai/v1/models` preflight. Only if that succeeds and `openai/gpt-oss-120b` is returned as active may A05 make one bounded `POST https://api.groq.com/openai/v1/responses` request using that model.

Provider errors are persisted only as sanitized status/type/code/message fields. The credential and raw generated response content must not be persisted. T004 remains unmet unless provider-reported usage, latency, official pricing-derived cost and a response fingerprint are all observed and strict downstream import passes.
