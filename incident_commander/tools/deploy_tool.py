from google.adk.tools import FunctionTool

def normalize_service(service: str) -> str:
    s = service.strip().lower()
    s = s.replace("-", " ").replace("_", " ")
    return " ".join(s.split())

def fetch_deployments(service: str) -> str:
    """
    Fetch recent deployments for a service.
    """
    service_key = normalize_service(service)

    deployments_data = {
        "payment service": "Last deployment: 2 hours ago",
        "auth service": "Last deployment: 30 minutes ago",
        "recommendation engine": "Last deployment: 1 day ago"
    }

    return deployments_data.get(service_key, f"No deployment info for service: {service}")

deploy_tool = FunctionTool(fetch_deployments)