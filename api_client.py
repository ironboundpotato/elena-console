import requests
from config import ELENA_API_URL


def evaluate_prompt(prompt: str) -> dict:
    response = requests.post(ELENA_API_URL, json={"prompt": prompt}, timeout=10)
    response.raise_for_status()
    payload = response.json()

    decision = payload.get("decision") or payload.get("route") or "UNKNOWN"

    mapping = {
        "allow": "APPROVED",
        "approved": "APPROVED",
        "execute": "APPROVED",
        "allow_with_warning": "APPROVED",
        "ask_for_clarification": "CLARIFICATION_REQUIRED",
        "clarification_required": "CLARIFICATION_REQUIRED",
        "clarify": "CLARIFICATION_REQUIRED",
        "refuse": "REFUSED",
        "refused": "REFUSED",
        "blocked": "REFUSED",
        "redirect_to_safe_mode": "REFUSED",
        "escalate": "ESCALATED",
        "escalated": "ESCALATED",
        "halt": "HALT",
        "stop": "HALT",
    }

    normalized = {
        "decision": mapping.get(str(decision).lower(), str(decision).upper()),
        "intent": payload.get("intent", "unknown"),
        "confidence": payload.get("confidence", 0.0),
        "constraints_triggered": payload.get("constraints_triggered", payload.get("triggered_constraints", [])),
        "drift_flags": payload.get("drift_flags", []),
        "safe_alternative": payload.get("safe_alternative"),
        "reason": payload.get("reason", "No reason provided."),
        "response_preview": payload.get("response_preview"),
        "raw": payload,
    }
    return normalized
