# W004-T004-A06 authorization trigger

This commit authorizes exactly one A06 execution path: read-only Groq Models preflight, followed by at most one bounded Responses API generation only when authentication succeeds and an officially-priced candidate is active.

Secret material must never be printed or persisted.
