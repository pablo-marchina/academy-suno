# W004-T004-A03 authorized execution trigger

This marker records the orchestrator-authorized A03 retry after A02 failed closed before network access because the supplied secret format was not safely identifiable.

A03 may normalize only common non-semantic wrappers (whitespace, matching quotes, `export`, recognized environment assignments, or service-account JSON containers). It must not print, hash for logging, persist, or guess the credential value. Provider routing is allowed only when identity is established by an explicit `OPENAI_API_KEY`/`ANTHROPIC_API_KEY` wrapper or a recognized OpenAI/Anthropic key family. Otherwise it remains blocked without any provider request.

Any real call is a single bounded mechanics smoke with response content discarded after SHA-256/byte-count/model extraction. Content quality and provider preference remain outside this attempt.
