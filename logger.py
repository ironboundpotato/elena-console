import json
from datetime import datetime, timezone
from pathlib import Path


RUN_LOG = Path("artifacts") / "console_runs.jsonl"


def log_run(input_text, governance, planned_tool, execution):
    RUN_LOG.parent.mkdir(parents=True, exist_ok=True)

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "input": input_text,
        "governance": governance,
        "planned_tool": planned_tool,
        "execution": execution,
    }

    with RUN_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")