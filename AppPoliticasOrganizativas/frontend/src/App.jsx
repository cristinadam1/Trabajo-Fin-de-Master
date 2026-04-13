import { useState, useEffect } from 'react'
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import GenerationForm from './components/GenerationForm'
import ResultsDisplay from './components/ResultsDisplay'
import GenerationList from './components/GenerationList'
import './App.css'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function App() {
  const [generations, setGenerations] = useState([])
  const [loading, setLoading] = useState(false)
  const [currentGeneration, setCurrentGeneration] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchGenerations()
  }, [])

  const fetchGenerations = async () => {
    try {
      const response = await fetch(`${API_URL}/api/generations`)
      if (response.ok) {
        const data = await response.json()
        setGenerations(data)
      }
    } catch (err) {
      console.error('Error al obtener las generaciones:', err)
    }
  }

  const handleGenerar = async (inputText) => {
    setLoading(true)
    setError(null)
    try {
      const response = await fetch(`${API_URL}/api/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ input_text: inputText }),
      })
      if (response.ok) {
        const data = await response.json()
        setCurrentGeneration(data)
        fetchGenerations()
      } else {
        const errData = await response.json()
        const errorMsg = errData.detail || 'Error al generar contenido'
        setError(errorMsg)
      }
    } catch (err) {
      setError('Error de conexión con el servidor. Verifica que el backend está funcionando')
    } finally {
      setLoading(false)
    }
  }

  const handleRegenerar = async (id) => {
    setLoading(true)
    setError(null)
    try {
      const response = await fetch(`${API_URL}/api/regenerate/${id}`, {
        method: 'POST',
      })
      if (response.ok) {
        const data = await response.json()
        setCurrentGeneration(data)
        fetchGenerations()
      }
    } catch (err) {
      setError('Error de conexión al regenerar. Intentalo de nuevo.')
    } finally {
      setLoading(false)
    }
  }

  const handleFavorito = async (id, isFavorite) => {
    try {
      await fetch(`${API_URL}/api/generations/${id}/favorite`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ is_favorite: isFavorite }),
      })
      if (currentGeneration?.id === id) {
        setCurrentGeneration({ ...currentGeneration, is_favorite: isFavorite })
      }
      fetchGenerations()
    } catch (err) {
      console.error('Error al cambiar a favorito:', err)
    }
  }

  const handleEliminar = async (id) => {
    try {
      await fetch(`${API_URL}/api/generations/${id}`, {
        method: 'DELETE',
      })
      if (currentGeneration?.id === id) {
        setCurrentGeneration(null)
      }
      fetchGenerations()
    } catch (err) {
      console.error('Error eliminando:', err)
    }
  }

  const handleVerDetalles = async (generation) => {
    try {
      const response = await fetch(`${API_URL}/api/generations/${generation.id}`)
      if (response.ok) {
        const data = await response.json()
        setCurrentGeneration(data)
      }
    } catch (err) {
      console.error('Error al obtener detalles:', err)
    }
  }

  return (
    <BrowserRouter>
      <div className="app">
        <header className="app-header">
          <h1>Generador de Políticas Organizativas</h1>
          <nav>
            <Link to="/">Inicio</Link>
            <Link to="/historial">Historial</Link>
          </nav>
        </header>

        <main className="app-main">
          {error && <div className="error-message">{error}</div>}
          
          <Routes>
            <Route
              path="/"
              element={
                <div className="home-page">
                  <GenerationForm onGenerate={handleGenerar} loading={loading} />
                  {currentGeneration && (
                    <ResultsDisplay
                      generation={currentGeneration}
                      onRegenerate={() => handleRegenerar(currentGeneration.id)}
                      onToggleFavorite={(fav) =>
                        handleFavorito(currentGeneration.id, fav)
                      }
                    />
                  )}
                </div>
              }
            />
            <Route
              path="/historial"
              element={
                <GenerationList
                  generations={generations}
                  onViewDetail={handleVerDetalles}
                  onRegenerate={handleRegenerar}
                  onToggleFavorite={handleFavorito}
                  onDelete={handleEliminar}
                />
              }
            />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}

export default App