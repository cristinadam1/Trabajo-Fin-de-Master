import GenerationCard from './GenerationCard'
import './GenerationList.css'

function GenerationList({
  generations,
  onVerDetalles,
  onRegenerar,
  onToggleFavorite,
  onEliminar,
}) {
  return (
    <div className="generation-list">
      <h2>Historial de Generaciones</h2>
      {generations.length === 0 ? (
        <p className="no-generations">No hay generaciones guardadas.</p>
      ) : (
        <div className="generations-grid">
          {generations.map((gen) => (
            <GenerationCard
              key={gen.id}
              generation={gen}
              onVerDetalles={onVerDetalles}
              onRegenerar={onRegenerar}
              onToggleFavorite={onToggleFavorite}
              onEliminar={onEliminar}
            />
          ))}
        </div>
      )}
    </div>
  )
}

export default GenerationList