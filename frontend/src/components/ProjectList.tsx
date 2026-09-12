import { useEffect, useState } from 'react'
import api from '../api'
import ProjectCard from './ProjectCard'

interface Project {
  id: number
  name: string
  repository_url: string
  branch: string
  created_at: string
}

interface Props {
  refreshKey: number
}

export default function ProjectList({ refreshKey }: Props) {
  const [projects, setProjects] = useState<Project[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    api.get('/projects')
      .then(res => setProjects(res.data))
      .finally(() => setLoading(false))
  }, [refreshKey])

  if (loading) return <p className="text-sm text-gray-500">Loading projects...</p>

  if (projects.length === 0) return (
    <p className="text-sm text-gray-500">No projects yet. Create one above.</p>
  )

  return (
    <div className="space-y-4">
      <h2 className="text-sm font-semibold text-gray-300">Projects</h2>
      {projects.map(project => (
        <ProjectCard key={project.id} project={project} />
      ))}
    </div>
  )
}