import TarjetaGeneracion from './TarjetaGeneracion'
import './ListaGeneraciones.css'

function ListaGeneraciones({
  generaciones,
  onVerDetalles,
  onToggleFavorito,
  onEliminar,
}) {
  return (
    <div className="lista-generaciones">
      <h2>Historial de Generaciones</h2>
      {generaciones.length === 0 ? (
        <p className="sin-generaciones">No hay generaciones guardadas.</p>
      ) : (
        <div className="generaciones-grid">
          {generaciones.map((gen) => (
            <TarjetaGeneracion
              key={gen.id}
              generacion={gen}
              onVerDetalles={onVerDetalles}
              onToggleFavorito={onToggleFavorito}
              onEliminar={onEliminar}
            />
          ))}
        </div>
      )}
    </div>
  )
}

export default ListaGeneraciones
