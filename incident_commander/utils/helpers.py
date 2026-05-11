import json
import os
from datetime import datetime


def save_run_to_file(run_data: dict, base_folder: str = "data/runs") -> str:
    """
    Save a workflow run to a timestamped JSON file.
    """
    os.makedirs(base_folder, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(base_folder, f"incident_run_{timestamp}.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(run_data, f, indent=2, ensure_ascii=False)

    return file_path


def extract_approval_required_actions(guardrail_text: str) -> list[str]:
    """
    Extract actions marked as APPROVAL REQUIRED from guardrail output.
    """
    actions = []

    for line in guardrail_text.splitlines():
        if "APPROVAL REQUIRED" in line:
            parts = line.split("**")
            if len(parts) >= 2:
                action = parts[1].strip()
                actions.append(action)
            else:
                actions.append(line.strip())

    return actions


def list_saved_runs(base_folder: str = "data/runs") -> list[str]:
    """
    List saved run files in reverse chronological order.
    """
    if not os.path.exists(base_folder):
        return []

    files = [
        f for f in os.listdir(base_folder)
        if f.endswith(".json")
    ]
    files.sort(reverse=True)
    return files