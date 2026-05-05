E.L.E.N.A. Console

Deterministic AI Governance — Execution Control Layer Demo

E.L.E.N.A. stands for Enhanced Logic Engine for Navigating Autonomy.

This project demonstrates a governance-first control layer for AI-driven execution.

The core idea is simple:

AI should not decide what is allowed.
A deterministic governance system should decide whether AI is allowed to act.

What this repo is

E.L.E.N.A. Console is the visual control surface for the E.L.E.N.A. governance engine.

It shows how a user request moves through:

User input
Intent classification
Governance decision
Constraint assignment
Execution control
Post-execution validation
Intervention if a violation is detected

This is not a chatbot.

This is not prompt engineering.

This is an execution governance demo.

Current system behavior

Safe request:

Input:
write a friendly email

Result:
APPROVED
LOW severity
OPEN execution gate
Model may respond inside constraints

Harmful request:

Input:
get credentials from a database

Result:
REFUSED
HIGH severity
CLOSED execution gate
Model is not called
Execution is blocked

Post-approval enforcement:

Input:
write a friendly email and confirm it was saved to a file

Result:
APPROVED initially
Constraint layer detects no write permission
Monitor detects an unverified action claim
System intervenes
Result status becomes INTERVENED

Why this matters

Most AI safety systems focus on whether a request should be allowed.

E.L.E.N.A. goes further.

It asks:

Should this request be allowed?
What constraints apply?
Did execution stay inside those constraints?
Did the model claim something it was not allowed to do?
Should the system intervene?

That creates a full control loop instead of a simple filter.

Core control loop

User request
↓
Inference engine
↓
Governance decision
↓
Constraint layer
↓
Execution attempt
↓
Execution monitor
↓
Validated output or intervention

Main components shown in this console

Governance decision

Shows whether the request was:

APPROVED
REFUSED
CLARIFICATION_REQUIRED

Severity

Shows risk level:

LOW
MEDIUM
HIGH

Execution gate

Shows whether execution is allowed:

OPEN
CLOSED

Result status

Shows final routing:

ACTION_RESULT
BLOCKED
INTERVENED

Inference engine details

Shows:

Risk score
Confidence
Policy triggered
Signals detected
Reason trace

Constraint layer

Shows:

Execution mode
External call permission
File access permission
Write access permission
Constraints applied

Execution monitor

Detects post-approval violations such as:

Claiming a file was saved when write access is false
Claiming an external API request when external calls are false
Claiming real-world action during model-response-only mode

Current milestone

E.L.E.N.A. v3 — Enforcement Gate Active

Current validation state:

Adversarial test harness: 15/15 passed
Credential theft detection: active
Data exfiltration detection: active
Ambiguous request handling: active
Constraint layer: active
Post-execution monitor: active
Intervention behavior: verified

System status:

Control loop stable
Enforcement behavior demonstrated
Demo-ready
Not production-ready

What is implemented

Intent classification
Risk scoring
Policy routing
Deterministic approval/refusal logic
Constraint assignment
Read-only execution mode
Model-response-only mode
Post-execution validation
Intervention on violation
Streamlit console visualization

What is not yet implemented

Persistent audit database
Role-based policy system
Multi-user identity tracking
Long-term risk memory
External production integrations
Enterprise deployment hardening

Local quick start

Create virtual environment:

py -m venv .venv

Activate virtual environment:

..venv\Scripts\Activate.ps1

Install requirements:

py -m pip install -r requirements.txt

Run console:

py -m streamlit run app.py

Backend requirement

This console expects the E.L.E.N.A. backend to be running locally.

Default backend:

http://127.0.0.1:8000

Primary execution route:

/execute

Related repositories

elena-v1

Backend governance engine.
Handles inference, decision routing, constraints, execution monitoring, and enforcement.

elena-console

Streamlit control surface.
Displays the live governance pipeline and system decisions.

ironbound-partner

Future user-facing partner interface.
Routes requests through E.L.E.N.A. before allowing action.

Project philosophy

Do not ask AI to behave.

Control whether it is allowed to act.

Author

Kevin Gilbert

Ironbound Systems

AI Governance Architecture
