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
}