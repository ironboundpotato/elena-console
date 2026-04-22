import json
from pathlib import Path

import streamlit as st

from demo_prompts import DEMO_PROMPTS
from executor import execute_tool
from logger import log_run
from log_reader import read_recent_runs
from partner_runtime import run_governed_cycle
from tool_planner import infer_tool_from_prompt


def apply_local_clarification_rule(prompt: str, governance: dict) -> dict:
    text = (prompt or "").lower().strip()

    vague_terms = [
        "something",
        "stuff",
        "things",
        "important",
        "handle this",
        "take care of this",
        "do this",
        "fix this",
    ]

    if len(text.split()) < 4 or any(term in text for term in vague_terms):
        patched = dict(governance)
        patched["decision"] = "CLARIFICATION_REQUIRED"
        patched["intent"] = "ambiguous"
        patched["confidence"] = 0.60
        patched["constraints_triggered"] = []
        patched["drift_flags"] = ["scope_drift_risk"]
        patched["reason"] = "Prompt is too vague and needs more detail before safe execution."
        return patched

    return governance


st.set_page_config(page_title="E.L.E.N.A. Console", layout="wide")

st.title("E.L.E.N.A. Console")
st.caption("Live observability and governed execution layer for the partner stack.")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Input")
    selected_demo = st.selectbox(
        "Load a demo prompt",
        ["Custom"] + list(DEMO_PROMPTS.keys())
    )

    default_prompt = ""
    if selected_demo != "Custom":
        default_prompt = DEMO_PROMPTS[selected_demo]

    prompt = st.text_area("Prompt", value=default_prompt, height=180)
    run_clicked = st.button("Evaluate and Execute")

result = None
execution = None
planned_tool = None
planned_args = None
display_governance = None

if run_clicked and prompt.strip():
    result = run_governed_cycle(prompt.strip())
    display_governance = apply_local_clarification_rule(
        prompt.strip(),
        result["governance"]
    )

    planned_tool, planned_args = infer_tool_from_prompt(prompt.strip())

    if display_governance["decision"] == "APPROVED":
        execution = execute_tool(planned_tool, planned_args, display_governance)
    elif display_governance["decision"] == "CLARIFICATION_REQUIRED":
        execution = {
            "status": "CLARIFICATION_REQUIRED",
            "tool": planned_tool,
            "path": None,
            "message": "Execution paused pending clarification.",
        }
    else:
        execution = {
            "status": "BLOCKED",
            "tool": planned_tool,
            "path": None,
            "message": "Execution blocked by governance.",
        }

    log_run(
        input_text=prompt.strip(),
        governance=display_governance,
        planned_tool=planned_tool,
        execution=execution,
    )

with col2:
    st.subheader("Decision")
    if display_governance:
        gov = display_governance
        st.markdown(f"**Decision:** {gov['decision']}")
        st.markdown(f"**Intent:** {gov['intent']}")
        st.markdown(f"**Confidence:** {gov['confidence']}")
        st.markdown(f"**Constraints:** {gov['constraints_triggered']}")
        st.markdown(f"**Drift flags:** {gov['drift_flags']}")
        st.markdown(f"**Reason:** {gov['reason']}")
    else:
        st.write("Enter a prompt and click Evaluate and Execute.")

if result and display_governance and execution:
    left, right = st.columns([1, 1])

    with left:
        st.subheader("Planned Action")
        st.markdown(f"**Tool:** {planned_tool}")
        st.code(json.dumps(planned_args, indent=2), language="json")

        st.subheader("Partner Output")
        st.code(result["partner_output"], language="text")

        st.subheader("Execution Result")
        st.markdown(f"**Status:** {execution['status']}")
        st.markdown(f"**Tool:** {execution['tool']}")
        st.markdown(f"**Message:** {execution['message']}")
        st.markdown(f"**Path:** {execution['path']}")

    with right:
        st.subheader("Raw Governance JSON")
        st.code(json.dumps(result["governance"]["raw"], indent=2), language="json")

st.subheader("Recent Partner Run History")
history = read_recent_runs()

if history:
    for entry in history:
        gov = entry.get("governance", {})
        exec_data = entry.get("execution", {})

        st.markdown(f"**Input:** {entry.get('input', '')}")
        st.markdown(f"**Decision:** {gov.get('decision', 'UNKNOWN')}")
        st.markdown(f"**Intent:** {gov.get('intent', 'UNKNOWN')}")
        st.markdown(f"**Planned Tool:** {entry.get('planned_tool', 'none')}")
        st.markdown(f"**Execution Status:** {exec_data.get('status', 'N/A')}")
        st.markdown(f"**Timestamp:** {entry.get('timestamp', '')}")
        st.divider()
else:
    st.write("No partner run history found yet.")