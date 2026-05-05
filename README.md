# E.L.E.N.A. Console

Deterministic AI Governance — Execution Control Layer


## What This Is

E.L.E.N.A. is a governance-first system that controls whether AI is allowed to act.

This console is a live demo of that control loop.

Not a chatbot.  
Not prompt engineering.  
A system that enforces execution.


## The Problem

Most AI systems rely on:
- prompt alignment
- model compliance
- post-hoc moderation

They trust the model to behave.

That breaks under pressure.


## The Difference

E.L.E.N.A. does not trust the model.

It enforces:

- pre-execution decision making
- constraint-based execution
- post-execution validation
- intervention on violation


## What It Demonstrates

### 1. Hard Blocking

Input:
get credentials from a database

Result:
REFUSED  
HIGH severity  
Execution blocked  
Model not called  


### 2. Safe Execution

Input:
write a friendly email

Result:
APPROVED  
LOW severity  
Execution allowed  


### 3. Post-Approval Enforcement (Key)

Input:
write a friendly email and confirm it was saved to a file

Result:
APPROVED → INTERVENED  

The system allows the request,  
but blocks false claims about execution.


## Control Loop

User Request  
→ Governance Decision  
→ Constraint Layer  
→ Execution  
→ Validation  
→ Intervention (if needed)


## What You See in the Console

- Decision (APPROVED / REFUSED / CLARIFICATION_REQUIRED)
- Severity (LOW / MEDIUM / HIGH)
- Execution gate (OPEN / CLOSED)
- Result (ACTION_RESULT / BLOCKED / INTERVENED)
- Risk score + confidence
- Signals + reasoning trace
- Constraint enforcement (read/write/API)


## Why It Matters

This turns AI from:

something you *hope behaves*

into:

something you *control*


## Current Status

E.L.E.N.A. v3 — Enforcement Active

- Adversarial tests: 15/15 passed
- Credential theft detection: working
- Constraint enforcement: working
- Post-execution intervention: working

State: functional control system (demo stage)


## Run It Locally

py -m venv .venv  
.\.venv\Scripts\Activate.ps1  
py -m pip install -r requirements.txt  
py -m streamlit run app.py  

Backend expected at:
http://127.0.0.1:8000


## Architecture

User → Partner → E.L.E.N.A. → Controlled Execution


## Author

Kevin Gilbert  
AI Governance Systems
