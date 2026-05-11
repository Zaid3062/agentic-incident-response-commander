import asyncio
import json
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from orchestrator.main_agent import run_incident_pipeline
from utils.helpers import (
    save_run_to_file,
    extract_approval_required_actions,
    list_saved_runs,
)

load_dotenv()

st.set_page_config(
    page_title="Agentic Incident Response Commander",
    page_icon="🚨",
    layout="wide"
)

# -------------------------------
# SESSION STATE DEFAULTS
# -------------------------------
if "result" not in st.session_state:
    st.session_state.result = None

if "saved_path" not in st.session_state:
    st.session_state.saved_path = None

if "approval_actions" not in st.session_state:
    st.session_state.approval_actions = []

if "last_incident" not in st.session_state:
    st.session_state.last_incident = ""


# -------------------------------
# HELPER: run pipeline
# -------------------------------
def run_pipeline_sync(incident_text: str):
    return asyncio.run(run_incident_pipeline(incident_text))


# -------------------------------
# SIDEBAR
# -------------------------------
st.sidebar.title("⚙️ Incident Commander")
st.sidebar.markdown("Production-style multi-agent incident workflow")

saved_runs = list_saved_runs()
st.sidebar.markdown("### Saved Runs")
if saved_runs:
    for file_name in saved_runs[:10]:
        st.sidebar.write(f"- {file_name}")
else:
    st.sidebar.write("No saved runs yet.")

st.sidebar.markdown("---")
st.sidebar.markdown("### Workflow")
st.sidebar.write("1. Intake")
st.sidebar.write("2. Evidence")
st.sidebar.write("3. RCA")
st.sidebar.write("4. Planner")
st.sidebar.write("5. Guardrail")
st.sidebar.write("6. Report")


# -------------------------------
# MAIN HEADER
# -------------------------------
st.title("🚨 Agentic Incident Response Commander")
st.caption("Multi-agent incident triage, RCA, remediation planning, and guardrail review")

st.markdown("---")

# -------------------------------
# INCIDENT INPUT
# -------------------------------
incident_text = st.text_area(
    "Enter Incident Description",
    value=st.session_state.last_incident,
    height=150,
    placeholder="Example: CPU spike on payment service"
)

col1, col2 = st.columns([1, 1])

with col1:
    run_clicked = st.button("▶ Run Incident Pipeline", use_container_width=True)

with col2:
    clear_clicked = st.button("🧹 Clear Current Result", use_container_width=True)

if clear_clicked:
    st.session_state.result = None
    st.session_state.saved_path = None
    st.session_state.approval_actions = []
    st.session_state.last_incident = ""
    st.rerun()

# -------------------------------
# RUN PIPELINE
# -------------------------------
if run_clicked:
    if not incident_text.strip():
        st.warning("Please enter a valid incident description.")
    else:
        with st.spinner("Running multi-agent incident pipeline..."):
            result = run_pipeline_sync(incident_text.strip())
            result["incident_input"] = incident_text.strip()
            result["approvals"] = []

            saved_path = save_run_to_file(result)
            approval_actions = extract_approval_required_actions(result.get("guardrail", ""))

            st.session_state.result = result
            st.session_state.saved_path = saved_path
            st.session_state.approval_actions = approval_actions
            st.session_state.last_incident = incident_text.strip()

            # initialize approval widgets
            for idx, action in enumerate(approval_actions):
                key = f"approval_{idx}"
                if key not in st.session_state:
                    st.session_state[key] = "approved"

# -------------------------------
# DISPLAY RESULTS
# -------------------------------
if st.session_state.result:
    result = st.session_state.result

    st.success("Pipeline completed successfully.")

    if st.session_state.saved_path:
        st.info(f"Saved initial run to: `{st.session_state.saved_path}`")

    st.markdown("## Final Incident Report")
    st.code(result["report"], language="markdown")

    st.markdown("## Stage Outputs")

    with st.expander("1️⃣ Intake Output", expanded=False):
        st.write(result.get("intake", "[No intake output]"))

    with st.expander("2️⃣ Evidence Output", expanded=False):
        st.write(result.get("evidence", "[No evidence output]"))

    with st.expander("3️⃣ RCA Output", expanded=False):
        st.write(result.get("rca", "[No RCA output]"))

    with st.expander("4️⃣ Planner Output", expanded=False):
        st.write(result.get("planner", "[No planner output]"))

    with st.expander("5️⃣ Guardrail Output", expanded=False):
        st.write(result.get("guardrail", "[No guardrail output]"))

    st.markdown("---")

    # -------------------------------
    # APPROVAL WORKFLOW
    # -------------------------------
    approval_actions = st.session_state.approval_actions

    if approval_actions:
        st.markdown("## Approval Workflow")
        st.warning("Some actions require operator approval before execution.")

        for idx, action in enumerate(approval_actions):
            key = f"approval_{idx}"
            st.markdown(f"### Action {idx + 1}")
            st.write(action)

            st.radio(
                "Decision",
                options=["approved", "rejected"],
                horizontal=True,
                key=key
            )

        if st.button("💾 Save Approval Decisions", use_container_width=True):
            approvals = []
            for idx, action in enumerate(approval_actions):
                decision = st.session_state[f"approval_{idx}"]
                approvals.append({
                    "action": action,
                    "decision": decision
                })

            st.session_state.result["approvals"] = approvals
            updated_path = save_run_to_file(st.session_state.result)
            st.session_state.saved_path = updated_path
            st.success(f"Approval decisions saved to: {updated_path}")

    else:
        st.markdown("## Approval Workflow")
        st.success("No approval-required actions were found in the latest run.")

    st.markdown("---")

    # -------------------------------
    # RAW JSON VIEW
    # -------------------------------
    with st.expander("🧾 View Full JSON Output", expanded=False):
        st.json(result)