import threading
import time
import httpx
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.project import Deployment
from app.services.docker_service import get_container_status


def check_deployment_health(deployment: Deployment, db: Session):
    if not deployment.port:
        return

    try:
        response = httpx.get(
            f"http://localhost:{deployment.port}/health",
            timeout=5.0
        )
        if response.status_code == 200:
            new_status = "running"
        else:
            new_status = "unhealthy"
    except Exception:
        # Can't reach the container
        container_status = get_container_status(deployment.container_name)
        if container_status == "not_found":
            new_status = "stopped"
        else:
            new_status = "unhealthy"

    if deployment.status != new_status:
        deployment.status = new_status
        db.commit()


def health_check_loop():
    while True:
        try:
            db = SessionLocal()
            active_deployments = (
                db.query(Deployment)
                .filter(Deployment.status.in_(["running", "unhealthy"]))
                .all()
            )
            for deployment in active_deployments:
                check_deployment_health(deployment, db)
            db.close()
        except Exception as e:
            print(f"Health check error: {e}")

        time.sleep(30)


def start_health_checker():
    thread = threading.Thread(target=health_check_loop, daemon=True)
    thread.start()