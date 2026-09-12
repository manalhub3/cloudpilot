import docker
import random
from datetime import datetime

client = docker.from_env()


def get_available_port(start: int = 8100, end: int = 8200) -> int:
    used_ports = set()
    for container in client.containers.list():
        for port_bindings in container.ports.values():
            if port_bindings:
                for binding in port_bindings:
                    used_ports.add(int(binding["HostPort"]))

    for port in range(start, end):
        if port not in used_ports:
            return port

    raise RuntimeError("No available ports in range")


def deploy_container(
    project_id: int,
    repository_url: str,
    branch: str,
    deployment_id: int,
) -> dict:
    container_name = f"cloudpilot-project-{project_id}-dep-{deployment_id}"
    port = get_available_port()

    # Pull or build the image
    # For now we use a pre-built image of the ai-document-assistant
    # Later we'll add git clone + docker build
    image = "ai-document-assistant-backend"

    try:
        container = client.containers.run(
            image=image,
            name=container_name,
            detach=True,
            ports={"8000/tcp": port},
            network="ai-document-assistant_default",
            environment={
                "DATABASE_URL": "postgresql://postgres:password@postgres:5432/ai_assistant",
                "AZURE_OPENAI_ENDPOINT": "placeholder",
                "AZURE_OPENAI_API_KEY": "placeholder",
                "AZURE_OPENAI_DEPLOYMENT": "placeholder",
                "AZURE_OPENAI_API_VERSION": "placeholder",
                "SECRET_KEY": "placeholder",
            }
        )
        return {
            "container_id": container.id,
            "container_name": container_name,
            "port": port,
            "status": "running",
        }
    except Exception as e:
        return {
            "container_id": None,
            "container_name": container_name,
            "port": port,
            "status": "failed",
            "error": str(e),
        }


def stop_container(container_name: str) -> bool:
    try:
        container = client.containers.get(container_name)
        container.stop()
        container.remove()
        return True
    except Exception:
        return False


def get_container_logs(container_name: str) -> str:
    try:
        container = client.containers.get(container_name)
        return container.logs(tail=100).decode("utf-8")
    except Exception as e:
        return f"Could not retrieve logs: {str(e)}"


def get_container_status(container_name: str) -> str:
    try:
        container = client.containers.get(container_name)
        return container.status
    except docker.errors.NotFound:
        return "not_found"
    except Exception:
        return "unknown"