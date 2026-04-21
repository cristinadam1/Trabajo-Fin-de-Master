import { Link } from 'react-router-dom'
import './Inicio.css'

function Inicio() {
  return (
    <div className="inicio">
      <div className="inicio-contenido">
        <h1>Generador de Políticas Organizativas</h1>
        
        <p className="inicio-descripcion">
        Esta herramienta permite generar políticas organizativas adaptadas al contexto específico de una empresa mediante el uso de modelos de lenguaje ejecutados en local. 
        A partir de una descripción del entorno empresarial, el sistema produce directrices alineadas con buenas prácticas en seguridad, cumplimiento y gestión de riesgos.
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
          Prueba el Generador
        </Link>
      </div>
    </div>
  )
}

export default Inicio
