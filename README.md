# elena-console

E.L.E.N.A. Console is a lightweight observability layer for the governed partner stack.

It visualizes the runtime path from user input to governance decision to final partner output.

## Architecture

**User -> Partner -> E.L.E.N.A. Gate -> Decision -> Allowed Response/Action**

## What this repo does

- sends prompts into the governed flow
- displays the returned governance decision
- shows partner-facing output
- reads recent JSONL run history from `ironbound-partner`

## Demo paths

- Approved
- Clarification Required
- Refused

## Quick start

```bash
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

Make sure `elena-v1` is already running locally at `http://127.0.0.1:8000/evaluate`.
