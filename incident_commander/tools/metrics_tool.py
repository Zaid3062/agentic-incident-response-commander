from google.adk.tools import FunctionTool

def normalize_service(service: str) -> str:
    s = service.strip().lower()
    s = s.replace("-", " ").replace("_", " ")
    return " ".join(s.split())

def fetch_metrics(service: str) -> str:
    """
    Fetch metrics for a service.
    """
    service_key = normalize_service(service)

    metrics_data = {
        "payment service": "CPU: 95%, Memory: 70%, Errors: High",
        "auth service": "CPU: 40%, Memory: 50%, Errors: Critical spike",
        "recommendation engine": "CPU: 60%, Memory: 92%, Errors: Moderate"
    }

    return metrics_data.get(service_key, f"No metrics available for service: {service}")

metrics_tool = FunctionTool(fetch_metrics)
