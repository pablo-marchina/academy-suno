# W004-T004-A02 authorized execution trigger

This marker records the orchestrator-authorized transition from preparation to one bounded real provider mechanics probe after the user confirmed `PROVIDER_API_KEY` is supplied.

Safety/validity constraints:

- exactly one branch-scoped run is authorized by the trigger commit message;
- the secret value must never be printed, committed, uploaded, or passed as a CLI argument;
- provider detection happens inside the GitHub runner from a recognized key prefix only and fails closed otherwise;
- OpenAI path uses `gpt-5.6-luna` at `https://api.openai.com/v1/responses` with the official pricing snapshot in this attempt;
- Anthropic path uses `claude-haiku-4-5-20251001` at `https://api.anthropic.com/v1/messages` with the official pricing snapshot in this attempt;
- output is bounded to 128 tokens;
- raw response content is not persisted, only SHA-256/byte count/provider-returned model plus mechanics telemetry;
- content quality remains outside this task and must come from independent W004-T005/T007 evidence.
