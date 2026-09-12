from sqlalchemy import Column, Integer, String, DateTime, func
from app.core.database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    repository_url = Column(String, nullable=False)
    branch = Column(String, default="main")
    created_at = Column(DateTime, server_default=func.now())


class Deployment(Base):
    __tablename__ = "deployments"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, nullable=False)
    status = Column(String, default="pending")
    container_id = Column(String, nullable=True)
    container_name = Column(String, nullable=True)
    port = Column(Integer, nullable=True)
    logs = Column(String, nullable=True)
    started_at = Column(DateTime, server_default=func.now())
    finished_at = Column(DateTime, nullable=True)