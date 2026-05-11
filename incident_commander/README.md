# Agentic Incident Response Commander

A production-style multi-agent incident response system built with **Google ADK**, **Gemini on Vertex AI**, and **Streamlit**.

This project automates the flow of incident triage, evidence collection, root-cause analysis, remediation planning, safety validation, and final report generation using an orchestrated set of specialized AI agents.

---

## 🚀 Project Overview

Traditional incident handling is manual, slow, and fragmented across multiple tools and teams.

This project demonstrates how a **multi-agent AI system** can assist an operations engineer by taking a raw incident description and automatically producing:

- structured incident understanding
- evidence summary
- likely root-cause analysis
- remediation plan
- guardrail / approval review
- final incident report
- saved audit trail for every run

---

## ✅ Key Features

- **Incident Intake Agent**  
  Parses incident descriptions into structured summaries.

- **Evidence Agent**  
  Collects simulated logs, metrics, and deployment information using tools.

- **RCA Agent**  
  Analyzes evidence and generates likely root causes with confidence levels.

- **Planner Agent**  
  Suggests remediation steps based on identified causes.

- **Guardrail Agent**  
  Classifies actions into:
  - SAFE
  - APPROVAL REQUIRED
  - BLOCKED

- **Report Agent**  
  Generates a final professional incident report.

- **Orchestrator**  
  Runs the full workflow automatically from one incident input.

- **Audit Trail Persistence**  
  Saves every run as a timestamped JSON file.

- **Streamlit UI**  
  Provides a demo-ready operator dashboard for running the workflow and reviewing outputs.

---

## 🧠 Architecture

```text
Incident Input
   ↓
Intake Agent
   ↓
Evidence Agent
   ↓
RCA Agent
   ↓
Planner Agent
   ↓
Guardrail Agent
   ↓
Report Agent
   ↓
Final Incident Report + Audit Trail