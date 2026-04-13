import { useState, useEffect } from 'react'
import './App.css'

function App() {
    const [generations, setGenerations] = useState([])
    const [loading, setLoading] = useState(false)
    const [currentGeneration, setCurrentGeneration] = useState(null)
    const [error, setError] = useState(null)
  
    useEffect(() => {
      fetchGenerations()
    }, [])
    
    const fetchGenerations = async () => {
        try {
          const response = await fetch(`${API_URL}/api/generations`)
          if (response.ok) {
            const data = await response.json()
            setGenerations(data)
          }
        } catch (err) {
          console.error('Error al obtener las generaciones:', err)
        }
      }

    const handleGenerate = async (inputText) => {
        setLoading(true)
        setError(null)
        try {
          const response = await fetch(`${API_URL}/api/generate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ input_text: inputText }),
          })
          if (response.ok) {
            const data = await response.json()
            setCurrentGeneration(data)
            fetchGenerations()
          } else {
            const errData = await response.json()
            const errorMsg = errData.detail || 'Error al generar contenido'
            setError(errorMsg)
          }
        } catch (err) {
          setError('Error de conexión con el servidor. Verifica que el backend está funcionando.')
        } finally {
          setLoading(false)
        }
      }
}