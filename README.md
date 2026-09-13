
# CloudPilot

A self-service platform for deploying and managing containerized AI applications. Built with FastAPI, React, PostgreSQL, and the Docker SDK for Python.

## What It Does

CloudPilot lets you:

- Register a project with a Git repository URL
- Deploy it as a Docker container with one click
- Monitor container health automatically every 30 seconds
- View live container logs
- Stop and restart deployments
- Track deployment history

## Architecture

React Dashboard
↓
CloudPilot API (FastAPI)
↓
Docker SDK for Python
↓
Docker Engine
↓
┌──────────────┬──────────────┐
│ AI App #1 │ AI App #2 │
│ port 8100 │ port 8101 │
└──────────────┴──────────────┘


## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React, TypeScript, Tailwind CSS, Vite |
| Backend | Python, FastAPI, SQLAlchemy |
| Database | PostgreSQL |
| Container Management | Docker SDK for Python |
| Health Monitoring | Background thread, httpx |
| CI | GitHub Actions |

## Project Structure

cloudpilot/
├── backend/
│ ├── app/
│ │ ├── api/ # projects, deployments routes
│ │ ├── core/ # config, database
│ │ ├── models/ # Project, Deployment models
│ │ └── services/ # docker_service, health_service
│ ├── requirements.txt
│ └── Dockerfile
└── frontend/
├── src/
│ ├── components/ # ProjectCard, ProjectList, CreateProject
│ └── api.ts
└── Dockerfile


## Getting Started

### Prerequisites

- Docker Desktop running
- Python 3.13+
- Node 22+

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

Start a PostgreSQL container:

```bash
docker run -d --name cloudpilot-db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=cloudpilot \
  -p 5433:5432 postgres:16
```

Create `backend/.env`:

DATABASE_URL=postgresql://postgres:password@localhost:5433/cloudpilot
SECRET_KEY=your_secret_key


Start the server:

```bash
uvicorn app.main:app --reload --port 8001
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/projects | Create a project |
| GET | /api/projects | List all projects |
| GET | /api/projects/{id} | Get a project |
| DELETE | /api/projects/{id} | Delete a project |
| POST | /api/projects/{id}/deploy | Deploy a container |
| GET | /api/projects/{id}/status | Get live container status |
| GET | /api/projects/{id}/logs | Get container logs |
| POST | /api/projects/{id}/stop | Stop the container |
| GET | /api/projects/{id}/deployments | Deployment history |

## Health Monitoring

CloudPilot runs a background thread that pings `GET /health` on every running container every 30 seconds. If the container stops responding, its status is automatically updated to `unhealthy` in the database and reflected in the UI.

## Demo Application

The application deployed and managed by CloudPilot is [AI Document Assistant](https://github.com/manalhub3/ai-document-assistant) — a RAG-powered document Q&A system.