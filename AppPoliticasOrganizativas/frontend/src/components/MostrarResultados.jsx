import './MostrarResultados.css'

function MostrarResultados({ generacion, onRegenerar, onToggleFavorito }) {
  return (
    <div className="mostrar-resultados">
      <div className="resultados-header">
        <h2>Resultados Generados</h2>
        <div className="resultados-acciones">
          <button
            className={`boton-favorito ${generacion.is_favorite ? 'active' : ''}`}
            onClick={() => onToggleFavorito(!generacion.is_favorite)}
          >
            {generacion.is_favorite ? '★ Favorito' : '☆ Favorito'}
          </button>
          <button className="boton-regenerar" onClick={onRegenerar}>
            Regenerar
          </button>
        </div>
      </div>

      <div className="resultados-input">
        <h3>Contexto</h3>
        <p>{generacion.input_text}</p>
      </div>

      <div className="resultados-secciones">
        <section className="seccion-resultado">
          <h3>📋 Políticas Organizativas</h3>
          <pre>{generacion.politicas}</pre>
        </section>

        <section className="seccion-resultado">
          <h3>✅ Buenas Prácticas</h3>
          <pre>{generacion.buenas_practicas}</pre>
        </section>

        <section className="seccion-resultado">
          <h3>⛔ Acciones Prohibidas</h3>
          <pre>{generacion.acciones_prohibidas}</pre>
        </section>

        <section className="seccion-resultado">
          <h3>🚨 Riesgos Identificados</h3>
          <pre>{generacion.riesgos}</pre>
        </section>

        <section className="seccion-resultado">
          <h3>📖 Explicación Justificativa</h3>
          <pre>{generacion.explicacion}</pre>
        </section>
      </div>
    </div>
  )
}

export default MostrarResultados
