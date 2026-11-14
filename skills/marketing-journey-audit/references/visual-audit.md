# Visual audit evidence

Capture the actual page before judging it. Use the browser available in the user's workspace. Follow its screenshot/export instructions rather than assuming a tool or account is installed.

## Capture

- Include the offer, headline, proof, primary CTA and the important next screen.
- Use a focused viewport or section capture. Add enough surrounding context to identify the page and element.
- Record URL, capture time, viewport width/height and visible state. A date on the website is not the capture date.
- Check the actual image format and dimensions. Screenshot pixels may differ from CSS pixels or the device-pixel ratio. For a viewport capture, scale x/width by image width / viewport width and y/height by image height / viewport height. Cropped or full-page captures need their actual origin and dimensions. Inspect alignment afterward.
- Preserve the original file. Do not change the page copy or hide UI to make the evidence look cleaner. Record a modal, consent banner, error or blocked step as the state actually seen.
- Use public screens without personal data. Do not embed an unredacted private image beneath a reversible overlay.

## Annotation style

Use a restrained black, off-white and lime palette. Apply thin dark outlines with a white halo, numbered circular markers and short matching finding cards. Add one to three focused callouts per image when possible.

Keep explanations outside the screenshot. Each numbered finding needs:

1. What is visible, in plain words.
2. Why it may matter to the agreed customer action.
3. A proposed next step.
4. A check or measure that could confirm or change the recommendation.

Label a claim as observed, a hypothesis or a proposal. Classify the action as Fix, Test or Need data. A useful existing element can be documented without calling it broken.

Keep contrast high on light and dark website backgrounds. Use whitespace around figures, readable source captions, a consistent number system and text labels for statuses. On small screens, allow the screenshot to scroll at a readable size and stack finding cards. Include a working Show original control. Print should retain the annotations and source caption.

A proposed redesign is a separate figure labeled Proposed. Never replace the evidence with the proposed version or imply a conversion lift from a screenshot.

## Build the appendix

The included Python helper supports PNG and JPEG captures. It embeds the unchanged source image into SVG and draws overlays above it. It rejects invalid dimensions, out-of-bounds highlights and missing metadata.

Place captures beside a manifest. Use paths relative to that manifest, and do not point outside its folder. Save this structure with real values:

```json
{
  "title": "Customer Journey Visual Audit",
  "business": "Business and offer being audited",
  "screens": [{
    "id": "S1",
    "file": "offer-original.jpg",
    "title": "Offer and primary CTA",
    "url": "https://example.com/offer",
    "captured_at": "2026-11-14T10:00:00Z",
    "viewport": {"width": 1280, "height": 720},
    "state": "Initial viewport, before selecting the CTA",
    "annotations": [{
      "id": "F1",
      "rect": [210, 400, 260, 50],
      "title": "Primary CTA",
      "status": "Need data",
      "observation": "Describe the actual visible element.",
      "why": "Explain its possible relationship to the agreed goal.",
      "next_step": "Propose a specific action without claiming an unmeasured defect.",
      "verify": "Name the observation or metric needed next."
    }]
  }]
}
```

The rectangle is `[x, y, width, height]` in source-image pixels, not percentages. An optional `badge: [x, y]` positions the number in nearby empty space when the default would cover evidence. The example coordinates are illustrative, not evidence for a real site. Replace every example value with actual observations.

Run:

```sh
python3 path/to/marketing-journey-audit/scripts/render_visual_audit.py --input visual-evidence/manifest.json --output Visual-Audit-Appendix.html
```

If Python is unavailable, create equivalent native HTML/SVG using this guide. The skill must not depend on a paid design tool.

## Review and handoff

Open the rendered HTML. Match every number to the original element at readable scale. Check rectangle placement, cropped labels, source captions, mobile layout and print preview. Test Show original and confirm that only annotation overlays disappear.

Keep the capture manifest and raw images locally. Share the self-contained HTML or an explicitly packaged report with working assets. Carry the full annotated evidence into Customer-Journey-Audit.html and the final strategy document, with the same finding IDs.
