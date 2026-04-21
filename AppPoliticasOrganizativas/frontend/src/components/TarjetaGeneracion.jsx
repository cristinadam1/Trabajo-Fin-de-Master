import { useState } from 'react'
import './TarjetaGeneracion.css'

function TarjetaGeneracion({
  generacion,
  onVerDetalles,
  onRegenerar,
  onToggleFavorito,
  onEliminar,
}) {
  const [regenerando, setRegenerando] = useState(false)

  const date = new Date(generacion.created_at).toLocaleDateString('es-ES', {
    año: 'numeric',
    mes: 'short',
    dia: 'numeric',
    hora: '2-digit',
    minuto: '2-digit',
  })

  const handleRegenerar = async () => {
    setRegenerando(true)
    try {
      await onRegenerar(generacion.id)
    } finally {
      setRegenerando(false)
    }
  }

  return (
    <div className={`tarjeta-generacion ${generacion.is_favorite ? 'favorito' : ''}`}>
      <div className="tarjeta-header">
        <span className="tarjeta-fecha">{date}</span>
        <button
          className="tarjeta-favorito"
          onClick={() => onToggleFavorito(generacion.id, !generacion.is_favorite)}
        >
          {generacion.is_favorite ? '★' : '☆'}
        </button>
      </div>
      <p className="tarjeta-preview">{generacion.input_text.substring(0, 150)}...</p>
      <div className="tarjeta-acciones">
        <button onClick={() => onVerDetalles(generacion)}>Ver</button>
        <button onClick={handleRegenerar} disabled={regenerando}>
          {regenerando ? 'Regenerando...' : 'Regenerar'}
        </button>
        <button className="boton-eliminar" onClick={() => onEliminar(generacion.id)}>
          Eliminar
        </button>
      </div>
    </div>
  )
}

export default TarjetaGeneracion