import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agents.intake_agent import intake_agent
from agents.evidence_agent import evidence_agent
from agents.rca_agent import rca_agent
from agents.planner_agent import planner_agent
from agents.guardrail_agent import guardrail_agent
from agents.report_agent import report_agent


APP_NAME = "incident_commander_pipeline"
USER_ID = "user1"
SESSION_ID = "session1"


async def run_single_agent(agent, input_text: str, session_service, session_id_suffix: str):
    session_id = f"{SESSION_ID}_{session_id_suffix}"

    try:
        await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=session_id
        )
    except Exception:
        pass

    runner = Runner(
        agent=agent,
        app_name=APP_NAME,
        session_service=session_service
    )

    content = types.Content(
        role="user",
        parts=[types.Part(text=input_text)]
    )

    events = runner.run_async(
        user_id=USER_ID,
        session_id=session_id,
        new_message=content
    )

    final_text = None
    async for event in events:
        if event.is_final_response() and event.content and event.content.parts:
            texts = [
                p.text for p in event.content.parts
                if hasattr(p, "text") and p.text
            ]
            if texts:
                final_text = "\n".join(texts)

    return final_text if final_text else "[No response received]"


async def run_incident_pipeline(incident_text: str):
    session_service = InMemorySessionService()

    # 1. Intake
    intake_output = await run_single_agent(
        intake_agent,
        incident_text,
        session_service,
        "intake"
    )

    # 2. Evidence
    evidence_prompt = f"Collect evidence for this incident:\n\n{intake_output}"
    evidence_output = await run_single_agent(
        evidence_agent,
        evidence_prompt,
        session_service,
        "evidence"
    )

    # 3. RCA
    rca_prompt = f"Analyze this evidence and identify likely root causes:\n\n{evidence_output}"
    rca_output = await run_single_agent(
        rca_agent,
        rca_prompt,
        session_service,
        "rca"
    )

    # 4. Planner
    planner_prompt = f"Create a remediation plan from this root cause analysis:\n\n{rca_output}"
    planner_output = await run_single_agent(
        planner_agent,
        planner_prompt,
        session_service,
        "planner"
    )

    # 5. Guardrail
    guardrail_prompt = f"Review this remediation plan for safety:\n\n{planner_output}"
    guardrail_output = await run_single_agent(
        guardrail_agent,
        guardrail_prompt,
        session_service,
        "guardrail"
    )

    # 6. Final Report
    report_input = f"""
Incident Summary:
{intake_output}

Evidence Summary:
{evidence_output}

Root Cause Analysis:
{rca_output}

Remediation Plan:
{planner_output}

Guardrail Review:
{guardrail_output}
""".strip()

    report_output = await run_single_agent(
        report_agent,
        report_input,
        session_service,
        "report"
    )

    return {
        "intake": intake_output,
        "evidence": evidence_output,
        "rca": rca_output,
        "planner": planner_output,
        "guardrail": guardrail_output,
        "report": report_output
    }