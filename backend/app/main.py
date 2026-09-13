from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.projects import router as projects_router
from app.api.deployments import router as deployments_router
from app.core import database
from app.core.database import engine
from app.services.health_service import start_health_checker

app = FastAPI(
    title="CloudPilot",
    description="AI Application Deployment Platform",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(projects_router, prefix="/api")
app.include_router(deployments_router, prefix="/api")


@app.on_event("startup")
def startup():
    database.Base.metadata.create_all(bind=engine)
    start_health_checker()


@app.get("/health")
def health():
    return {"status": "healthy"}