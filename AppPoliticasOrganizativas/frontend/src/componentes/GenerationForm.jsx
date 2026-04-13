import { useState } from 'react'
import './GenerationForm.css'

function GenerationForm({ onGenerar, loading }) {
  const [inputText, setInputText] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (inputText.trim()) {
      onGenerar(inputText)
    }
  }

  return (
    <form className="generation-form" onSubmit={handleSubmit}>
      <label htmlFor="input-text">
        Describe el contexto organizativo, técnico o empresarial:
      </label>
      <textarea
        id="input-text"
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
        placeholder="Ej: Empresa de desarrollo software que trabaja con datos sensibles de clientes..."
        rows={6}
        disabled={loading}
      />
      <button type="submit" disabled={loading || !inputText.trim()}>
        {loading ? 'Generando...' : 'Generar Políticas'}
      </button>
    </form>
  )
}

export default GenerationForm