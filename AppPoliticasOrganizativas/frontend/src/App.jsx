import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import Inicio from './pages/Inicio'
import Generador from './pages/Generador'
import Historial from './pages/Historial'
import MarcoNormativo from './pages/MarcoNormativo'
import './App.css'

function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <header className="app-header">
          <h1>Generador de Políticas Organizativas</h1>
          <nav>
            <Link to="/">Inicio</Link>
            <Link to="/generador">Generador</Link>
            <Link to="/historial">Historial</Link>
            <Link to="/marco-normativo">Marco Normativo</Link>
          </nav>
        </header>

        <main className="app-main">
          <Routes>
            <Route path="/" element={<Inicio />} />
            <Route path="/generador" element={<Generador />} />
            <Route path="/historial" element={<Historial />} />
            <Route path="/marco-normativo" element={<MarcoNormativo />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}

export default App
