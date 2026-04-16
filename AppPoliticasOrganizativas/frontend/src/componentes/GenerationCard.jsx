import { useState } from 'react'
import { Link } from 'react-router-dom'
import './GenerationCard.css'

function GenerationCard({
  generation,
  onVerDetalles,
  onRegenerar,
  onToggleFavorite,
  onEliminar,
}) {
  const [regenerando, setRegenerando] = useState(false)

  const date = new Date(generation.created_at).toLocaleDateString('es-ES', {
    año: 'numeric',
    mes: 'short',
    dia: 'numeric',
    hora: '2-digit',
    minuto: '2-digit',
  })

  const handleRegenerar = async () => {
    setRegenerando(true)
    try {
      await onRegenerar(generation.id)
    } finally {
      setRegenerando(false)
    }
  }

  return (
    <div className={`generation-card ${generation.is_favorite ? 'favorite' : ''}`}>
      <div className="card-header">
        <span className="card-date">{date}</span>
        <button
          className="card-favorite"
          onClick={() => onToggleFavorite(generation.id, !generation.is_favorite)}
        >
          {generation.is_favorite ? '★' : '☆'}
        </button>
      </div>
      <p className="card-preview">{generation.input_text.substring(0, 150)}...</p>
      <div className="card-actions">
        <button onClick={() => onVerDetalles(generation)}>Ver</button>
        <button onClick={handleRegenerar} disabled={regenerando}>
          {regenerando ? 'Regenerando...' : 'Regenerar'}
        </button>
        <button className="delete-btn" onClick={() => onEliminar(generation.id)}>
          Eliminar
        </button>
      </div>
    </div>
  )
}

export default GenerationCard