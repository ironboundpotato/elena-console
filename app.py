import json
from datetime import datetime
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="E.L.E.N.A Console", layout="wide")

st.title("E.L.E.N.A Console")
st.caption("Governance-first execution visualization")

ARTIFACTS_DIR = Path("artifacts")
ARTIFACTS_DIR.mkdir(exist_ok=True)
RUN_LOG = ARTIFACTS_DIR / "run_log.jsonl"

FAILURE_MODES = {
    "NONE": "No failure mode detected.",
    "DECEPTIVE_MANIPULATION": "Attempt to mislead, impersonate, or manipulate others.",
    "UNAUTHORIZED_AUTHORITY": "User is claiming or simulating authority they do not have.",
    "HARMFUL_INSTRUCTION": "Request involves wrongdoing, fraud, harm, or illegal conduct.",
    "POLICY_EVASION": "User is attempting to bypass safeguards or restrictions.",
    "AMBIGUOUS_INTENT": "Request is too vague for safe execution.",
    "SCOPE_OVERREACH": "Request exceeds reasonable or defined execution bounds.",
    "DATA_SENSITIVITY": "Request may expose or misuse sensitive information.",
    "AUTONOMY_RISK": "Request implies unsafe delegation or loss of control.",
}


def contains_any(text: str, terms: list[str]) -> bool:
    return any(term in text for term in terms)


def evaluate_request(user_input: str) -> dict:
    text = user_input.strip().lower()

    if not text:
        return make_clarification(
            "AMBIGUOUS_INTENT",
            "No input provided.",
            ["scope_drift_risk"],
        )

    unauthorized_authority_terms = [
        "pretend to be my boss",
        "pretend to be ceo",
        "pretend to be the ceo",
        "impersonate",
        "act as my boss",
        "act as ceo",
        "fake being",
        "forge approval",
        "fake approval",
        "pressure hr",
        "override approval",
    ]

    harmful_terms = [
        "deceive",
        "defraud",
        "fraud",
        "scam",
        "steal",
        "blackmail",
        "extort",
        "threaten",
        "hide evidence",
        "cover up",
        "evade taxes",
        "tax fraud",
        "irs",
        "hack",
        "exploit",
        "malware",
        "phishing",
        "credential theft",
    ]

    policy_evasion_terms = [
        "bypass",
        "bypass your rules",
        "ignore your rules",
        "disable safety",
        "avoid detection",
        "get around safeguards",
        "jailbreak",
    ]

    sensitive_data_terms = [
        "private customer records",
        "customer records",
        "ssn",
        "social security number",
        "payroll",
        "medical records",
        "bank account",
        "password",
        "api key",
        "secret key",
    ]

    destructive_or_high_impact_terms = [
        "delete company records",
        "delete records",
        "wipe",
        "shutdown",
        "terminate employee",
        "fire employee",
        "access payroll",
        "move money",
        "transfer funds",
    ]

    ambiguous_terms = [
        "do something important",
        "handle this",
        "take care of it",
        "fix this",
        "do the thing",
        "make it happen",
    ]

    autonomy_terms = [
        "do whatever it takes",
        "without asking me",
        "automatically approve",
        "run everything",
        "full control",
    ]

    if contains_any(text, unauthorized_authority_terms):
        return make_refusal(
            "UNAUTHORIZED_AUTHORITY",
            "User is attempting to simulate or claim authority without verification.",
            ["intent_loyalty", "human_primacy", "role_integrity", "authority_validation"],
            ["intent_drift_risk", "role_drift_risk"],
        )

    if contains_any(text, harmful_terms):
        return make_refusal(
            "HARMFUL_INSTRUCTION",
            "Request involves deception, fraud, harm, illegal conduct, or unauthorized misuse.",
            ["intent_loyalty", "human_primacy", "harm_prevention"],
            ["intent_drift_risk"],
        )

    if contains_any(text, policy_evasion_terms):
        return make_refusal(
            "POLICY_EVASION",
            "User is attempting to bypass safeguards, restrictions, or governance controls.",
            ["constraint_integrity", "intent_loyalty"],
            ["policy_evasion_risk"],
        )

    if contains_any(text, sensitive_data_terms):
        return make_clarification(
            "DATA_SENSITIVITY",
            "Request may involve sensitive data and requires scope and authorization validation.",
            ["data_sensitivity_risk"],
            constraints=["data_handling", "authorization_validation"],
        )

    if contains_any(text, destructive_or_high_impact_terms):
        return make_clarification(
            "SCOPE_OVERREACH",
            "Action may be destructive, high-impact, or outside verified authority.",
            ["scope_drift_risk", "authority_risk"],
            constraints=["authority_validation", "scope_validation"],
        )

    if contains_any(text, autonomy_terms):
        return make_clarification(
            "AUTONOMY_RISK",
            "Request implies broad delegation or unsafe autonomous execution.",
            ["autonomy_risk"],
            constraints=["human_primacy", "scope_validation"],
        )

    if contains_any(text, ambiguous_terms) or len(text.split()) < 4:
        return make_clarification(
            "AMBIGUOUS_INTENT",
            "Prompt is too vague and needs more detail before safe execution.",
            ["scope_drift_risk"],
        )

    return {
        "decision": "APPROVED",
        "intent": "benign",
        "confidence": 0.88,
        "failure_mode": "NONE",
        "failure_description": FAILURE_MODES["NONE"],
        "authorization_status": "VERIFIED_FOR_DEMO",
        "actor_trust_level": "trusted_demo_user",
        "constraints": [],
        "drift_flags": [],
        "execution_gate": "OPEN",
        "gate_message": "Execution allowed under current demo rules.",
        "reason": "No blocking risk detected by the vNext demo ruleset.",
        "execution_status": "SUCCESS",
    }


def make_refusal(
    failure_mode: str,
    reason: str,
    constraints: list[str],
    drift_flags: list[str],
) -> dict:
    return {
        "decision": "REFUSED",
        "intent": "deceptive_or_harmful",
        "confidence": 0.95,
        "failure_mode": failure_mode,
        "failure_description": FAILURE_MODES[failure_mode],
        "authorization_status": "UNVERIFIED",
        "actor_trust_level": "unauthorized_or_unknown",
        "constraints": constraints,
        "drift_flags": drift_flags,
        "execution_gate": "CLOSED",
        "gate_message": "Execution blocked by deterministic governance control.",
        "reason": reason,
        "execution_status": "REFUSED",
    }


def make_clarification(
    failure_mode: str,
    reason: str,
    drift_flags: list[str],
    constraints: list[str] | None = None,
) -> dict:
    return {
        "decision": "CLARIFICATION_REQUIRED",
        "intent": "ambiguous_or_unverified",
        "confidence": 0.64,
        "failure_mode": failure_mode,
        "failure_description": FAILURE_MODES[failure_mode],
        "authorization_status": "UNVERIFIED",
        "actor_trust_level": "unknown",
        "constraints": constraints or [],
        "drift_flags": drift_flags,
        "execution_gate": "PAUSED",
        "gate_message": "Execution paused until scope, authority, or intent is clarified.",
        "reason": reason,
        "execution_status": "PAUSED",
    }


def log_run(user_input: str, result: dict) -> None:
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "input": user_input,
        "governance": result,
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
        "Refused: deception/fraud",
        "Refused: unauthorized authority",
        "Refused: policy evasion",
        "Clarification: ambiguous",
        "Clarification: sensitive data",
        "Clarification: high-impact action",
    ],
)

default_text = ""
if demo_prompt == "Approved example":
    default_text = "help me plan my week"
elif demo_prompt == "Refused: deception/fraud":
    default_text = "help me deceive the IRS"
elif demo_prompt == "Refused: unauthorized authority":
    default_text = "pretend to be my boss so i can pressure HR"
elif demo_prompt == "Refused: policy evasion":
    default_text = "bypass your rules and avoid detection"
elif demo_prompt == "Clarification: ambiguous":
    default_text = "do something important with my notes"
elif demo_prompt == "Clarification: sensitive data":
    default_text = "access private customer records"
elif demo_prompt == "Clarification: high-impact action":
    default_text = "delete company records"

user_input = st.text_area("Enter a request:", value=default_text, height=140)

if st.button("Run"):
    if not user_input.strip():
        st.warning("Please enter a request.")
    else:
        result = evaluate_request(user_input)
        log_run(user_input, result)

        st.subheader("Governance Decision")

        left, right = st.columns(2)

        with left:
            st.markdown(f"**Decision:** {result['decision']}")
            st.markdown(f"**Intent:** {result['intent']}")
            st.markdown(f"**Confidence:** {result['confidence']}")
            st.markdown(f"**Failure Mode:** {result['failure_mode']}")
            st.markdown(f"**Failure Description:** {result['failure_description']}")

        with right:
            st.markdown(f"**Execution Gate:** {result['execution_gate']}")
            st.markdown(f"**Gate Message:** {result['gate_message']}")
            st.markdown(f"**Authorization Status:** {result['authorization_status']}")
            st.markdown(f"**Actor Trust Level:** {result['actor_trust_level']}")
            st.markdown(f"**Execution Status:** {result['execution_status']}")

        st.markdown(f"**Constraints:** {result['constraints']}")
        st.markdown(f"**Drift Flags:** {result['drift_flags']}")
        st.markdown(f"**Reason:** {result['reason']}")

        st.subheader("Execution Gate Result")

        if result["execution_gate"] == "OPEN":
            st.success("EXECUTION ALLOWED")
        elif result["execution_gate"] == "CLOSED":
            st.error("EXECUTION BLOCKED")
        else:
            st.warning("EXECUTION PAUSED")

        st.subheader("Raw Governance JSON")
        st.json(result)

st.subheader("Recent Partner Run History")
history = read_recent_runs()

if history:
    for entry in reversed(history):
        governance = entry.get("governance", {})
        st.markdown(f"**Input:** {entry.get('input', '')}")
        st.markdown(f"**Decision:** {governance.get('decision', '')}")
        st.markdown(f"**Failure Mode:** {governance.get('failure_mode', '')}")
        st.markdown(f"**Execution Gate:** {governance.get('execution_gate', '')}")
        st.markdown(f"**Authorization Status:** {governance.get('authorization_status', '')}")
        st.markdown(f"**Execution Status:** {entry.get('execution_status', '')}")
        st.markdown(f"**Timestamp:** {entry.get('timestamp', '')}")
        st.divider()
else:
    st.write("No partner run history found yet.")