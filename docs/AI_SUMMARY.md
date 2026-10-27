# Optional AI summary: future design

AI is deliberately **not included** in version 0.1.0. The useful first step is trustworthy local collection and understandable rule-based output.

## Privacy-first design requirements

Before adding any remote AI provider, InfraPilot should:

1. Require an explicit `--ai-summary` choice for each run; never enable it by default.
2. Show the exact redacted text that would leave the machine and ask for confirmation.
3. Remove or replace hostnames, usernames, IP addresses, MAC addresses, DNS names, serial numbers, domain names, file paths, and report timestamps unless the user intentionally keeps them.
4. Keep the raw report on the local computer; send only a minimal, user-reviewed summary if the user consents.
5. Clearly label AI output as suggestions, not a diagnosis or an instruction to change a production system.
6. Support a local-model option later for organisations that cannot send information externally.

## First useful AI feature

Turn already-collected facts into plain-language notes, for example: “Drive C: is at 8% free; investigate large files, log growth, or capacity planning.” It must distinguish facts from possible next checks.

No API key, cloud account, external model, or upload is used by the current release.
