import { useState, useEffect } from 'react'
import FormularioGeneracion from '../components/FormularioGeneracion'
import MostrarResultados from '../components/MostrarResultados'
import TarjetaGeneracion from '../components/TarjetaGeneracion'
import './Generador.css'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function Generador() {
  const [loading, setLoading] = useState(false)
  const [generacionActual, setGeneracionActual] = useState(null)
  const [error, setError] = useState(null)
  const [mostrarHistorial, setMostrarHistorial] = useState(false)
  const [generaciones, setGeneraciones] = useState([])
  const [loadingHistorial, setLoadingHistorial] = useState(false)

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

  useEffect(() => {
    fetchGeneraciones()
  }, [])

  const handleGenerar = async (inputText) => {
    setLoading(true)
    setError(null)
    try {
      const response = await fetch(`${API_URL}/api/generar`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ input_text: inputText }),
      })
      if (response.ok) {
        const data = await response.json()
        setGeneracionActual(data)
        fetchGeneraciones()
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

  const handleMostrarHistorial = async () => {
    if (!mostrarHistorial) {
      await fetchGeneraciones()
    }
    setMostrarHistorial(!mostrarHistorial)
  }

  const handleVerDetalles = async (generacion) => {
    setLoadingHistorial(true)
    try {
      const response = await fetch(`${API_URL}/api/generaciones/${generacion.id}`)
      if (response.ok) {
        const data = await response.json()
        setGeneracionActual(data)
        setMostrarHistorial(false)
      }
    } catch (err) {
      console.error('Error al obtener detalles:', err)
    } finally {
      setLoadingHistorial(false)
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
    <div className="generador">
      {error && <div className="error-message">{error}</div>}
      
      <FormularioGeneracion onGenerar={handleGenerar} loading={loading} />
      
      {generacionActual && (
        <MostrarResultados
          generacion={generacionActual}
          onRegenerar={() => handleRegenerar(generacionActual.id)}
          onToggleFavorito={(fav) =>
            handleFavorito(generacionActual.id, fav)
          }
        />
      )}

      <div className="generador-historial">
        <button 
          className="generador-historial-boton" 
          onClick={handleMostrarHistorial}
        >
          {mostrarHistorial ? '▼' : '▶'} Ver historial ({generaciones.length})
        </button>

        {mostrarHistorial && (
          <div className="generador-historial-contenido">
            {loadingHistorial ? (
              <p>Cargando...</p>
            ) : generaciones.length === 0 ? (
              <p>No hay generaciones guardadas.</p>
            ) : (
              <div className="generador-historial-grid">
                {generaciones.map((gen) => (
                  <TarjetaGeneracion
                    key={gen.id}
                    generacion={gen}
                    onVerDetalles={handleVerDetalles}
                    onRegenerar={handleRegenerar}
                    onToggleFavorito={handleFavorito}
                    onEliminar={handleEliminar}
                  />
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default Generador
