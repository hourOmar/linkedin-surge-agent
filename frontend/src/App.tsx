import { useEffect, useState } from 'react'
import './App.css'

const BACKEND_URL = 'http://localhost:8000'

function App() {
  const [status, setStatus] = useState<string>('checking...')

  useEffect(() => {
    fetch(`${BACKEND_URL}/health`)
      .then((res) => res.json())
      .then((data) => setStatus(data.status))
      .catch(() => setStatus('unreachable'))
  }, [])

  return (
    <section id="center">
      <h1>ENTROGX LinkedIn Surge Agent</h1>
      <p>
        Backend status: <strong>{status}</strong>
      </p>
    </section>
  )
}

export default App
