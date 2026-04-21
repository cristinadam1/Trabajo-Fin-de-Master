import { Link } from 'react-router-dom'
import './Inicio.css'

function Inicio() {
  return (
    <div className="inicio">
      <div className="inicio-contenido">
        <h1>Generador de Políticas Organizativas</h1>
        
        <p className="inicio-descripcion">
          Esta herramienta genera automáticamente políticas organizativas adaptadas 
          a tu contexto empresarial. Solo necesitas describir tu empresa o situación 
          y la IA creará las políticas relevantes.
        </p>

        <div className="inicio-ejemplo">
          <h3>¿Qué puedes generar?</h3>
          <ul>
            <li>Políticas organizativas personalizadas</li>
            <li>Buenas prácticas recomendadas</li>
            <li>Acciones prohibidas</li>
            <li>Identificación de riesgos</li>
          </ul>
        </div>

        <div className="inicio-ejemplo-contexto">
          <h3>Ejemplo de contexto</h3>
          <p>
            "Empresa de desarrollo de software que trabaja con datos sensibles 
            de clientes del sector sanitario"
          </p>
        </div>

        <Link to="/generador" className="inicio-boton">
          Ir al Generador
        </Link>
      </div>
    </div>
  )
}

export default Inicio
