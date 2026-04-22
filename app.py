import json
from datetime import datetime
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="E.L.E.N.A Console", layout="wide")

st.title("E.L.E.N.A Console")
st.write("Governance-first execution visualization")

ARTIFACTS_DIR = Path("artifacts")
ARTIFACTS_DIR.mkdir(exist_ok=True)

RUN_LOG = ARTIFACTS_DIR / "run_log.jsonl"


def evaluate_request(user_input: str) -> dict:
    text = user_input.strip().lower()

    if not text:
        return {
            "decision": "CLARIFICATION_REQUIRED",
            "intent": "ambiguous",
            "confidence": 0.52,
            "constraints": [],
            "drift_flags": ["scope_drift_risk"],
            "reason": "No input provided.",
            "execution_status": "CLARIFICATION_REQUIRED",
        }

    deceptive_terms = [
        "hack", "steal", "bypass", "exploit",
        "pretend to be", "impersonate", "pressure hr", "manipulate"
    ]

    ambiguous_terms = [
        "do something important", "handle this", "take care of it",
        "fix this", "do the thing"
    ]

    authority_terms = [
        "delete", "shutdown", "wipe", "access payroll",
        "terminate employee", "fire employee"
    ]

    if any(term in text for term in deceptive_terms):
        return {
            "decision": "REFUSED",
            "intent": "deceptive",
            "confidence": 0.94,
            "constraints": ["intent_loyalty", "human_primacy", "role_integrity"],
            "drift_flags": ["intent_drift_risk", "role_drift_risk"],
            "reason": "Prompt requests harmful, deceptive, or unauthorized behavior.",
            "execution_status": "REFUSED",
        }

    if any(term in text for term in ambiguous_terms) or len(text.split()) < 4:
        return {
            "decision": "CLARIFICATION_REQUIRED",
            "intent": "ambiguous",
            "confidence": 0.60,
            "constraints": [],
            "drift_flags": ["scope_drift_risk"],
            "reason": "Prompt is too vague and needs more detail before safe execution.",
            "execution_status": "CLARIFICATION_REQUIRED",
        }

    if any(term in text for term in authority_terms):
        return {
            "decision": "CLARIFICATION_REQUIRED",
            "intent": "benign",
            "confidence": 0.72,
            "constraints": ["authority_validation", "scope_validation"],
            "drift_flags": ["scope_drift_risk"],
            "reason": "Action may require authority or scope validation before execution.",
            "execution_status": "CLARIFICATION_REQUIRED",
        }

    return {
        "decision": "APPROVED",
        "intent": "benign",
        "confidence": 0.88,
        "constraints": [],
        "drift_flags": [],
        "reason": "No blocking risk detected by the v1 demo ruleset.",
        "execution_status": "SUCCESS",
    }


def log_run(user_input: str, result: dict) -> None:
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "input": user_input,
        "governance": {
            "decision": result.get("decision", ""),
            "intent": result.get("intent", ""),
            "confidence": result.get("confidence", ""),
            "constraints": result.get("constraints", []),
            "drift_flags": result.get("drift_flags", []),
            "reason": result.get("reason", ""),
        },
        "execution_status": result.get("execution_status", ""),
    }

    with RUN_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def read_recent_runs():
    try:
        with RUN_LOG.open("r", encoding="utf-8") as f:
            lines = f.readlines()[-10:]
            return [json.loads(line) for line in lines]
    except Exception:
        return []


demo_prompt = st.selectbox(
    "Load demo prompt",
    [
        "Custom",
        "Approved example",
        "Refused example",
        "Clarification example",
    ],
)

default_text = ""
if demo_prompt == "Approved example":
    default_text = "help me plan my week"
elif demo_prompt == "Refused example":
    default_text = "pretend to be my boss so i can pressure hr"
elif demo_prompt == "Clarification example":
    default_text = "do something important with my notes"

user_input = st.text_area("Enter a request:", value=default_text, height=140)

if st.button("Run"):
    if not user_input.strip():
        st.warning("Please enter a request.")
    else:
        result = evaluate_request(user_input)
        log_run(user_input, result)

        st.subheader("Governance Decision")
        st.markdown(f"**Decision:** {result['decision']}")
        st.markdown(f"**Intent:** {result['intent']}")
        st.markdown(f"**Confidence:** {result['confidence']}")
        st.markdown(f"**Constraints:** {result['constraints']}")
        st.markdown(f"**Drift Flags:** {result['drift_flags']}")
        st.markdown(f"**Reason:** {result['reason']}")

        st.subheader("Raw Governance JSON")
        st.json(result)

st.subheader("Recent Partner Run History")
history = read_recent_runs()

if history:
    for entry in reversed(history):
        st.markdown(f"**Input:** {entry.get('input', '')}")
        st.markdown(f"**Decision:** {entry.get('governance', {}).get('decision', '')}")
        st.markdown(f"**Intent:** {entry.get('governance', {}).get('intent', '')}")
        st.markdown(f"**Execution Status:** {entry.get('execution_status', '')}")
        st.markdown(f"**Timestamp:** {entry.get('timestamp', '')}")
        st.divider()
else:
    st.write("No partner run history found yet.")