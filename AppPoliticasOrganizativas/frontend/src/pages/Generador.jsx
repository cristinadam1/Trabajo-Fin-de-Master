import { useState, useEffect } from 'react'
import FormularioGeneracion from '../components/FormularioGeneracion'
import MostrarResultados from '../components/MostrarResultados'
import './Generador.css'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function Generador() {
  const [loading, setLoading] = useState(false)
  const [generacionActual, setGeneracionActual] = useState(null)
  const [error, setError] = useState(null)

  const fetchGeneraciones = async () => {
    try {
      const response = await fetch(`${API_URL}/api/generaciones`)
      if (response.ok) {
        await response.json()
      }
    } catch (err) {
      console.error('Error al obtener las generaciones:', err)
    }
  }

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
    </div>
  )
}

export default Generador
