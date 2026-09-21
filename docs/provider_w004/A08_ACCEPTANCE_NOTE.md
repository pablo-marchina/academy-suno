# W004-T004-A08 acceptance note

The accepted Groq mechanics run used the provider-documented OpenAI-compatible Python client (`openai==2.11.0`) with base URL `https://api.groq.com/openai/v1`.

Earlier raw `urllib` attempts A04-A07 were not accepted. A07 isolated Cloudflare error 1010 on the raw client path; A08 is the first accepted observed provider run and is the only attempt in this sequence eligible for canonical T004 integration.
