---
name: marketing-journey-audit
description: Create a visual customer journey audit with actual screenshots, precise numbered annotations and evidence-linked recommendations for offers, CTAs and conversion steps.
---

# Customer journey audit

Start with the agreed offer and primary customer action. Map only the route actually observed. Mark unobserved steps with a dashed style and a clear label.
For each step, record the customer's question, visible answer, required action, evidence and possible friction. Inspect existing help and alternative routes before proposing new ones.
Capture the offer, headline, proof, primary CTA and important next steps through the available browser, or use supplied screenshots. Keep the original image unchanged, record the URL, capture time, viewport and visible state, and reuse existing evidence. Inspect mobile when relevant to the question. Do not submit a form or enter private details merely to complete the map.
Read [the visual audit guide](references/visual-audit.md) before preparing annotations. Use precise regions in screenshot pixel coordinates, numbered markers, and readable finding cards outside the image. Prefer focused viewport or section captures over an unreadable full-page thumbnail. Do not cover the evidence with paragraphs or invent a screen you could not inspect.
Prioritize the strongest findings in the summary and include the detailed visual evidence. Give each an observed fact, possible consequence, classification (Fix, Test or Need data), recommended next step and its measurement check. A screenshot may also document a useful existing element; do not label every observation as a defect.
A checked defect may justify a fix. A plausible improvement needs a test. Missing evidence needs a data request. Extra steps and cross-domain forms do not prove abandonment or broken tracking.
If metrics are available, compare matching cohorts, event definitions and completed observation windows. A call-button click is not a completed call; a Next click is not completed registration.
If metrics are missing, request the smallest baseline that supports the decision. Never fabricate an overall marketing score or conversion loss.

## Output

Create Customer-Journey-Audit.html with annotated screenshots and update section customer-journey. Keep the raw images and a capture manifest beside the report. Embed images into the shareable HTML where practical so they survive report assembly.
Use scripts/render_visual_audit.py to build a styled evidence appendix from actual captures and a manifest, or follow its design in native HTML/SVG. It adds overlays without changing the source pixels. Python 3 is sufficient; no third-party imaging package is needed.
Verify every highlight against the original at readable size. Check labels, scaling, contrast, source metadata and mobile/print layout. If screenshot capture is unavailable, request images or label the visual evidence missing instead of substituting a fabricated page.

## Working rules

Use the materials the user supplies. Read .agents/marketing-business-context.md and the actual existing reports when available. A filename alone is not the report contents.
Ask once for missing information that could change the result. The user may proceed with unknowns.
Research permitted public pages when browsing is available. Record the URL and date checked. A supplied URL is not evidence that it was opened. If access fails, ask for page text or record a research task.
Keep observed facts, customer statements, provider claims, assumptions and proposals distinct. Preserve product labels and sample limits. Do not invent metrics, customer quotes, people, budgets, sources or performance.
Use plain words, short bullets, a useful diagram or compact comparison, and a small source list. No decorative scores or unsupported earnings claims.
Create local draft files only. Sharing, publishing, account access, messages and spending require their own authorization.

## Report continuity

Each output must work as a standalone report. Add or update its matching section in Marketing-Strategy-and-Action-Plan.html while preserving all other sections and sources. Start the master if absent. Missing sections remain missing, not invented.
If files cannot be written, return the report content and intended filename. Mark owners, targets, budgets and copy as proposed until agreed.
