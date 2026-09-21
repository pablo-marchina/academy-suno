# W004-T004-A07 authorization trigger

Authorize one read-only Groq Models preflight with sanitized diagnostics. If and only if that preflight returns 200 and an officially-priced GPT-OSS candidate is active, authorize at most one bounded Responses API generation. Secret material must never be printed or persisted.
