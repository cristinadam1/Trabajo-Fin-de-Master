import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import ListaGeneraciones from '../components/ListaGeneraciones'
import MostrarResultados from '../components/MostrarResultados'
import './Historial.css'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function Historial() {
  const [generaciones, setGeneraciones] = useState([])
  const [loading, setLoading] = useState(false)
  const [generacionActual, setGeneracionActual] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchGeneraciones()
  }, [])

  const fetchGeneraciones = async () => {
    try {
      const response = await fetch(`${API_URL}/api/generaciones`)
      if (response.ok) {
        const data = await response.json()
        setGeneraciones(data)
      }
    } catch (err) {
      console.error('Error al obtener las generaciones:', err)
    }
  }

  const handleVerDetalles = async (generacion) => {
    try {
      const response = await fetch(`${API_URL}/api/generaciones/${generacion.id}`)
      if (response.ok) {
        const data = await response.json()
        setGeneracionActual(data)
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
        setGeneracionActual(data)
        fetchGeneraciones()
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
      if (generacionActual?.id === id) {
        setGeneracionActual({ ...generacionActual, is_favorite: isFavorite })
      }
      fetchGeneraciones()
    } catch (err) {
      console.error('Error al cambiar a favorito:', err)
    }
  }

  const handleEliminar = async (id) => {
    try {
      await fetch(`${API_URL}/api/generaciones/${id}`, {
        method: 'DELETE',
      })
      if (generacionActual?.id === id) {
        setGeneracionActual(null)
      }
      fetchGeneraciones()
    } catch (err) {
      console.error('Error eliminando:', err)
    }
  }

  return (
    <div className="historial">
      {error && <div className="error-message">{error}</div>}
      
      {!generacionActual ? (
        <ListaGeneraciones
          generaciones={generaciones}
          onVerDetalles={handleVerDetalles}
          onRegenerar={handleRegenerar}
          onToggleFavorito={handleFavorito}
          onEliminar={handleEliminar}
        />
      ) : (
        <div>
          <button onClick={() => setGeneracionActual(null)}>
            Volver al historial
          </button>
          <MostrarResultados
            generacion={generacionActual}
            onRegenerar={() => handleRegenerar(generacionActual.id)}
            onToggleFavorito={(fav) =>
              handleFavorito(generacionActual.id, fav)
            }
          />
        </div>
      )}
    </div>
  )
}

export default Historial
