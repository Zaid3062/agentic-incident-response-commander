from google.adk.tools import FunctionTool

def normalize_service(service: str) -> str:
    s = service.strip().lower()
    s = s.replace("-", " ").replace("_", " ")
    return " ".join(s.split())

def fetch_logs(service: str) -> str:
    """
    Fetch recent logs for a service.
    """
    service_key = normalize_service(service)

    logs_data = {
        "payment service": "ERROR: CPU usage at 95%. Thread pool exhausted.",
        "auth service": "ERROR: Login failures increased after deployment.",
        "recommendation engine": "WARNING: Memory usage continuously rising."
    }

    return logs_data.get(service_key, f"No logs found for service: {service}")

logs_tool = FunctionTool(fetch_logs)