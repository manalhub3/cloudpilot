from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.project import Project

router = APIRouter()


class ProjectCreate(BaseModel):
    name: str
    repository_url: str
    branch: str = "main"


@router.post("/projects", status_code=status.HTTP_201_CREATED)
def create_project(data: ProjectCreate, db: Session = Depends(get_db)):
    project = Project(
        name=data.name,
        repository_url=data.repository_url,
        branch=data.branch
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.get("/projects")
def list_projects(db: Session = Depends(get_db)):
    return db.query(Project).all()


@router.get("/projects/{project_id}")
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()
    return {"message": f"Project {project_id} deleted"}