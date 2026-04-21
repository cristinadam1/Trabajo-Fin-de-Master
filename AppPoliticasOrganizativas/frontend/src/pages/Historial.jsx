import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import GenerationList from '../componentes/GenerationList'
import ResultsDisplay from '../componentes/ResultsDisplay'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function Historial() {
  const [generations, setGenerations] = useState([])
  const [loading, setLoading] = useState(false)
  const [currentGeneration, setCurrentGeneration] = useState(null)
  const [error, setError] = useState(null)
  const navigate = useNavigate()

  useEffect(() => {
    fetchGenerations()
  }, [])

  const fetchGenerations = async () => {
    try {
      const response = await fetch(`${API_URL}/api/generaciones`)
      if (response.ok) {
        const data = await response.json()
        setGenerations(data)
      }
    } catch (err) {
      console.error('Error al obtener las generaciones:', err)
    }
  }

  const handleVerDetalles = async (generation) => {
    try {
      const response = await fetch(`${API_URL}/api/generaciones/${generation.id}`)
      if (response.ok) {
        const data = await response.json()
        setCurrentGeneration(data)
      }
    } catch (err) {
      console.error('Error al obtener detalles:', err)
    }
  }

  const handleRegenerar = async (id) => {
    setLoading(true)
    setError(null)
    try {
      const response = await fetch(`${API_URL}/api/regenerar/${id}`, {
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
      await fetch(`${API_URL}/api/generaciones/${id}/favorito`, {
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
      await fetch(`${API_URL}/api/generaciones/${id}`, {
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

  return (
    <div className="historial">
      {error && <div className="error-message">{error}</div>}
      
      {!currentGeneration ? (
        <GenerationList
          generations={generations}
          onVerDetalles={handleVerDetalles}
          onRegenerar={handleRegenerar}
          onToggleFavorite={handleFavorito}
          onEliminar={handleEliminar}
        />
      ) : (
        <div>
          <button onClick={() => setCurrentGeneration(null)}>
            Volver al historial
          </button>
          <ResultsDisplay
            generation={currentGeneration}
            onRegenerar={() => handleRegenerar(currentGeneration.id)}
            onToggleFavorite={(fav) =>
              handleFavorito(currentGeneration.id, fav)
            }
          />
        </div>
      )}
    </div>
  )
}

export default Historial
