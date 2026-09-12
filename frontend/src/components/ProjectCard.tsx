import { useState } from 'react'
import api from '../api'

interface Project {
  id: number
  name: string
  repository_url: string
  branch: string
  created_at: string
}

interface DeploymentStatus {
  status: string
  container_name: string
  port: number | null
  url: string | null
}

export default function ProjectCard({ project }: { project: Project }) {
  const [deploying, setDeploying] = useState(false)
  const [stopping, setStopping] = useState(false)
  const [deploymentStatus, setDeploymentStatus] = useState<DeploymentStatus | null>(null)
  const [logs, setLogs] = useState<string | null>(null)
  const [showLogs, setShowLogs] = useState(false)
  const [errorMsg, setErrorMsg] = useState<string | null>(null)

  const deploy = async () => {
    setDeploying(true)
    setErrorMsg(null)
    try {
      const res = await api.post(`/projects/${project.id}/deploy`)
      setDeploymentStatus({
        status: res.data.status,
        container_name: res.data.container_name,
        port: res.data.port,
        url: res.data.url,
      })
    } catch (err: any) {
      setErrorMsg(err.response?.data?.detail || 'Deployment failed')
    } finally {
      setDeploying(false)
    }
  }

  const fetchStatus = async () => {
    try {
      const res = await api.get(`/projects/${project.id}/status`)
      setDeploymentStatus(res.data)
    } catch {
      setErrorMsg('Could not fetch status')
    }
  }

  const fetchLogs = async () => {
    try {
      const res = await api.get(`/projects/${project.id}/logs`)
      setLogs(res.data.logs)
      setShowLogs(true)
    } catch {
      setErrorMsg('Could not fetch logs')
    }
  }

  const stopContainer = async () => {
    setStopping(true)
    try {
      await api.post(`/projects/${project.id}/stop`)
      setDeploymentStatus(prev => prev ? { ...prev, status: 'stopped' } : null)
    } catch {
      setErrorMsg('Could not stop container')
    } finally {
      setStopping(false)
    }
  }

  const statusColor = (s: string) => {
    if (s === 'running') return 'text-green-400'
    if (s === 'stopped') return 'text-yellow-400'
    if (s === 'failed') return 'text-red-400'
    return 'text-gray-400'
  }

  return (
    <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
      <div className="flex items-start justify-between">
        <div>
          <h3 className="text-sm font-semibold text-white">{project.name}</h3>
          <p className="text-xs text-gray-500 mt-0.5">{project.repository_url}</p>
          <p className="text-xs text-gray-600 mt-0.5">Branch: {project.branch}</p>
        </div>
        {deploymentStatus && (
          <span className={`text-xs font-medium ${statusColor(deploymentStatus.status)}`}>
            ● {deploymentStatus.status}
          </span>
        )}
      </div>

      {deploymentStatus?.url && deploymentStatus.status === 'running' && (
        <a
          href={deploymentStatus.url}
          target="_blank"
          rel="noreferrer"
          className="mt-2 inline-block text-xs text-blue-400 hover:underline"
        >
          {deploymentStatus.url}
        </a>
      )}

      {errorMsg && <p className="mt-2 text-xs text-red-400">{errorMsg}</p>}

      <div className="mt-4 flex flex-wrap gap-2">
        <button
          onClick={deploy}
          disabled={deploying}
          className="text-xs bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white px-3 py-1.5 rounded-lg transition-colors"
        >
          {deploying ? 'Deploying...' : 'Deploy'}
        </button>
        <button
          onClick={fetchStatus}
          className="text-xs bg-gray-800 hover:bg-gray-700 text-gray-300 px-3 py-1.5 rounded-lg transition-colors"
        >
          Status
        </button>
        <button
          onClick={fetchLogs}
          className="text-xs bg-gray-800 hover:bg-gray-700 text-gray-300 px-3 py-1.5 rounded-lg transition-colors"
        >
          Logs
        </button>
        <button
          onClick={stopContainer}
          disabled={stopping}
          className="text-xs bg-red-900 hover:bg-red-800 disabled:opacity-50 text-red-300 px-3 py-1.5 rounded-lg transition-colors"
        >
          {stopping ? 'Stopping...' : 'Stop'}
        </button>
      </div>

      {showLogs && logs && (
        <div className="mt-4">
          <div className="flex items-center justify-between mb-1">
            <p className="text-xs text-gray-500">Container logs</p>
            <button
              onClick={() => setShowLogs(false)}
              className="text-xs text-gray-600 hover:text-gray-400"
            >
              Hide
            </button>
          </div>
          <pre className="bg-gray-950 border border-gray-800 rounded-lg p-3 text-xs text-green-400 overflow-x-auto max-h-48 overflow-y-auto whitespace-pre-wrap">
            {logs}
          </pre>
        </div>
      )}
    </div>
  )
}