import './ResultsDisplay.css'

function ResultsDisplay({ generation, onRegenerar, onToggleFavorite }) {
  return (
    <div className="results-display">
      <div className="results-header">
        <h2>Resultados Generados</h2>
        <div className="results-actions">
          <button
            className={`favorite-btn ${generation.is_favorite ? 'active' : ''}`}
            onClick={() => onToggleFavorite(!generation.is_favorite)}
          >
            {generation.is_favorite ? '★ Favorito' : '☆ Favorito'}
          </button>
          <button className="regenerate-btn" onClick={onRegenerar}>
            Regenerar
          </button>
        </div>
      </div>

      <div className="results-input">
        <h3>Contexto</h3>
        <p>{generation.input_text}</p>
      </div>

      <div className="results-sections">
        <section className="result-section">
          <h3>📋 Políticas Organizativas</h3>
          <pre>{generation.politicas}</pre>
        </section>

        <section className="result-section">
          <h3>✅ Buenas Prácticas</h3>
          <pre>{generation.buenas_practicas}</pre>
        </section>

        <section className="result-section">
          <h3>⛔ Acciones Prohibidas</h3>
          <pre>{generation.acciones_prohibidas}</pre>
        </section>

        <section className="result-section">
          <h3>🚨 Riesgos Identificados</h3>
          <pre>{generation.riesgos}</pre>
        </section>

        <section className="result-section">
          <h3>📖 Explicación Justificativa</h3>
          <pre>{generation.explicacion}</pre>
        </section>
      </div>
    </div>
  )
}

export default ResultsDisplay