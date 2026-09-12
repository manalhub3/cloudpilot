from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.database import get_db
from app.models.project import Project, Deployment
from app.services.docker_service import (
    deploy_container,
    stop_container,
    get_container_logs,
    get_container_status,
)

router = APIRouter()


@router.post("/projects/{project_id}/deploy", status_code=status.HTTP_201_CREATED)
def deploy_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    deployment = Deployment(project_id=project_id, status="deploying")
    db.add(deployment)
    db.commit()
    db.refresh(deployment)

    result = deploy_container(
        project_id=project_id,
        repository_url=project.repository_url,
        branch=project.branch,
        deployment_id=deployment.id,
    )

    deployment.status = result["status"]
    deployment.container_id = result.get("container_id")
    deployment.container_name = result.get("container_name")
    deployment.port = result.get("port")
    deployment.logs = result.get("error")
    deployment.finished_at = datetime.utcnow()
    db.commit()
    db.refresh(deployment)

    return {
        "deployment_id": deployment.id,
        "status": deployment.status,
        "container_name": deployment.container_name,
        "port": deployment.port,
        "url": f"http://localhost:{deployment.port}" if deployment.port else None,
    }


@router.get("/projects/{project_id}/deployments")
def list_deployments(project_id: int, db: Session = Depends(get_db)):
    return db.query(Deployment).filter(Deployment.project_id == project_id).all()


@router.get("/projects/{project_id}/status")
def get_status(project_id: int, db: Session = Depends(get_db)):
    deployment = (
        db.query(Deployment)
        .filter(Deployment.project_id == project_id)
        .order_by(Deployment.started_at.desc())
        .first()
    )
    if not deployment:
        raise HTTPException(status_code=404, detail="No deployments found")

    live_status = get_container_status(deployment.container_name)
    return {
        "deployment_id": deployment.id,
        "status": live_status,
        "container_name": deployment.container_name,
        "port": deployment.port,
        "url": f"http://localhost:{deployment.port}" if deployment.port else None,
    }


@router.get("/projects/{project_id}/logs")
def get_logs(project_id: int, db: Session = Depends(get_db)):
    deployment = (
        db.query(Deployment)
        .filter(Deployment.project_id == project_id)
        .order_by(Deployment.started_at.desc())
        .first()
    )
    if not deployment:
        raise HTTPException(status_code=404, detail="No deployments found")

    logs = get_container_logs(deployment.container_name)
    return {"logs": logs}


@router.post("/projects/{project_id}/stop")
def stop_project(project_id: int, db: Session = Depends(get_db)):
    deployment = (
        db.query(Deployment)
        .filter(Deployment.project_id == project_id)
        .order_by(Deployment.started_at.desc())
        .first()
    )
    if not deployment:
        raise HTTPException(status_code=404, detail="No deployments found")

    success = stop_container(deployment.container_name)
    if success:
        deployment.status = "stopped"
        db.commit()
        return {"message": "Container stopped successfully"}

    raise HTTPException(status_code=500, detail="Failed to stop container")