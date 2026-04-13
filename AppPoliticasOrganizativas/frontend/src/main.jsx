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
}