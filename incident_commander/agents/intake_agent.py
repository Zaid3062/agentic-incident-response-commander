from google.adk.agents.llm_agent import LlmAgent

intake_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="intake_agent",
    description="Analyzes incoming incident",
    instruction="""
You are an incident intake agent.

Your job:
- Extract service name
- Extract issue type
- Estimate severity (low, medium, high)

Return structured output like:

{
  "service": "...",
  "issue": "...",
  "severity": "..."
}
"""
)