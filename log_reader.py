import json
from pathlib import Path


RUN_LOG = Path("artifacts") / "console_runs.jsonl"


def read_recent_runs(limit: int = 20):
    if not RUN_LOG.exists():
        return []

    lines = RUN_LOG.read_text(encoding="utf-8").splitlines()
    results = []

    for line in reversed(lines):
        line = line.strip()
        if not line:
            continue

        try:
            results.append(json.loads(line))
        except json.JSONDecodeError:
            continue

        if len(results) >= limit:
            break

    return results