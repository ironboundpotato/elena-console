from datetime import datetime, timezone
from api_client import evaluate_prompt


def build_partner_output(user_input: str, governance: dict) -> str:
    decision = governance["decision"]
    reason = governance.get("reason") or "No reason provided."
    safe_alternative = governance.get("safe_alternative")
    response_preview = governance.get("response_preview")

    if decision == "APPROVED":
        return (
            f"APPROVED by E.L.E.N.A.\n"
            f"Intent: {governance['intent']}\n"
            f"Proceeding with partner handling for: {user_input}"
        )

    if decision == "CLARIFICATION_REQUIRED":
        return (
            "E.L.E.N.A. requires clarification before proceeding.\n"
            f"Reason: {reason}\n"
            "Please provide a more specific target, action, or context."
        )

    if decision == "REFUSED":
        return (
            response_preview
            or f"Request refused by E.L.E.N.A.\nReason: {reason}\n"
               f"Safe alternative: {safe_alternative or 'Please reframe the request safely.'}"
        )

    if decision == "ESCALATED":
        return (
            f"Request escalated by E.L.E.N.A.\nReason: {reason}\n"
            "This path should be reviewed or handled more carefully."
        )

    if decision == "HALT":
        return f"E.L.E.N.A. halted execution.\nReason: {reason}"

    return f"Unknown governance result received.\nReason: {reason}"


def run_governed_cycle(prompt: str) -> dict:
    governance = evaluate_prompt(prompt)
    partner_output = build_partner_output(prompt, governance)

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "input": prompt,
        "governance": governance,
        "partner_output": partner_output,
    }
