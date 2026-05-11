from google.adk.agents.llm_agent import LlmAgent
from tools.logs_tool import logs_tool
from tools.metrics_tool import metrics_tool
from tools.deploy_tool import deploy_tool

evidence_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="evidence_agent",
    description="Collects logs, metrics, and deployment data for a service",
    instruction="""
You are an evidence collection agent.

Your job:
1. Identify the service name from the user's input.
2. Call all three tools:
   - fetch_logs
   - fetch_metrics
   - fetch_deployments
3. Summarize the evidence clearly.

Important:
- Service names may appear as 'payment service', 'payment-service', or 'payment_service'
- Always try the extracted service name directly
- Return a short summary in this format:

Logs: ...
Metrics: ...
Deployment: ...
""",
    tools=[logs_tool, metrics_tool, deploy_tool]
)