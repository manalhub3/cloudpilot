import { useState } from 'react'
import ProjectList from './components/ProjectList'
import CreateProject from './components/CreateProject'

export default function App() {
  const [refreshKey, setRefreshKey] = useState(0)

  const onProjectCreated = () => setRefreshKey(k => k + 1)

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      <header className="border-b border-gray-800 px-6 py-4">
        <div className="max-w-5xl mx-auto flex items-center justify-between">
          <div>
            <h1 className="text-lg font-semibold tracking-tight">CloudPilot</h1>
            <p className="text-xs text-gray-500">AI Application Deployment Platform</p>
          </div>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-6 py-8 space-y-8">
        <CreateProject onCreated={onProjectCreated} />
        <ProjectList refreshKey={refreshKey} />
      </main>
    </div>
  )
}