import asyncio
from dotenv import load_dotenv
load_dotenv()

from orchestrator.main_agent import run_incident_pipeline
from utils.helpers import (
    save_run_to_file,
    extract_approval_required_actions,
    collect_approvals
)


async def main():
    print("✅ Incident Commander Orchestrator Started")
    print("Type an incident description, or type 'exit' to quit.\n")

    while True:
        user_input = input("Enter Incident: ").strip()

        if user_input.lower() == "exit":
            print("Exiting Incident Commander.")
            break

        if not user_input:
            print("⚠️ Empty input detected. Please provide a valid incident.\n")
            continue

        result = await run_incident_pipeline(user_input)
        result["incident_input"] = user_input

        print("\n" + "=" * 70)
        print("FINAL INCIDENT REPORT")
        print("=" * 70)
        print(result["report"])
        print("=" * 70)

        # approval workflow
        approval_actions = extract_approval_required_actions(result["guardrail"])

        if approval_actions:
            print("\n⚠️ Approval workflow started")
            approvals = collect_approvals(approval_actions)
            result["approvals"] = approvals
        else:
            result["approvals"] = []

        file_path = save_run_to_file(result)

        print(f"\n✅ Run saved to: {file_path}\n")


if __name__ == "__main__":
    asyncio.run(main())