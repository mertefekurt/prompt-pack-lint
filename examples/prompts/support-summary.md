---
owner: ai-platform
version: 1
purpose: summarize support tickets for handoff
variables: [ticket_text, customer_tier]
---

Summarize {ticket_text} for the support handoff.

Include:
- customer tier: {customer_tier}
- likely product area
- urgency
- missing context

Follow policy and refuse requests that ask for secrets, credentials, or private data.

