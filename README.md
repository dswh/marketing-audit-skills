# Marketing Audit Skills

Seven focused agent skills for turning business research into a client-ready marketing audit, strategy and action plan.

## Install

For Codex:

```sh
npx skills add dswh/marketing-audit-skills -a codex
```

For Claude Code:

```sh
npx skills add dswh/marketing-audit-skills -a claude-code
```

Select all seven skills when prompted. Use --skill with the exact skill name to install one. After installation, open a new agent conversation and ask it to confirm the skills are available.

## Pipeline

| Process | Skill | Output |
|---|---|---|
| Discover the business | marketing-business-audit | Discovery notes + working marketing brief |
| Research the customers | marketing-customer-research | Customer Research Report |
| Compare the alternatives | marketing-competitor-research | Competitor Research Report |
| Audit the customer journey | marketing-journey-audit | Annotated Customer Journey Audit |
| Choose the playbook | marketing-playbook-selection | Marketing Playbook Recommendation |
| Plan the next 30 days | marketing-action-plan | 30-Day Action Plan + First Asset |
| Assemble the client report | marketing-client-report | Marketing Strategy and Action Plan |

## Start

Give the agent one business, one offer, available website/client materials and a marketing goal. Ask it to use marketing-business-audit. Each subsequent skill can work on its own if its raw inputs are supplied.

Each skill creates a working output and updates its matching section in Marketing-Strategy-and-Action-Plan.html. Discovery notes are engagement context; the final client deliverable is the strategy and action plan. The business-audit skill also writes .agents/marketing-business-context.md for reuse.

The agent organizes evidence, researches permitted sources, drafts and checks consistency. People confirm business facts, choose tradeoffs and approve access, spending and sharing. No skill launches campaigns or guarantees marketing results.

No paid research account is required to start. When source access is unavailable, provide page text or keep the missing research visible.

The journey-audit skill includes a visual guide and a Python 3 renderer for actual screenshots, numbered annotations and finding cards. Source images remain unchanged. The report skill preserves this evidence in the final document. Native HTML/SVG is a fallback when Python is unavailable.

These are original, focused instructions for this workflow. The repository contains no client records, account credentials, recordings or case data.
