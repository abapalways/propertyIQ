# Task 9 — UI Screenshot (PENDING)

> **STATUS: PENDING LIVE RUN.** The screenshot `task9_ui_screenshot.png`
> requires launching the Gradio app against a live OpenAI key and capturing a
> real query result. No usable key was available when the code was written
> ("write code now, run later"), so no PNG was fabricated. This file documents
> exactly how to capture it.

## How to capture

```
# with a valid OPENAI_API_KEY in .env:
python src/ingest.py     # build the Chroma store (one time)
python src/app.py        # launches Gradio with a public share=True link
```

Then in the UI:

1. Set the **Buyer profile** dropdown to `B001 — David and Elena Torres`.
2. Send the query: `Find 3-bed homes under $450K near good schools in Austin`.
3. Screenshot the response and save it as
   `docs/evidence/task9_ui_screenshot.png`.

## What the screenshot must show

- A grounded shortlist for **B001 (Torres Family)**.
- **L_PINE_101 included** and surfaced as the top match.
- **L_ELM_124 excluded** — the response header shows the rejection-memory note
  ("Rejection memory removed (not shown): L_ELM_124"), since B001 already
  rejected it.

The app builds and runs headlessly today (verified: `build_demo()` returns a
`ChatInterface`, 17-buyer dropdown, graceful message when no key is present);
only the live model call and screenshot capture are deferred.
