import { Link } from 'react-router-dom'
import './Inicio.css'

function Inicio() {
  return (
    <div className="inicio">
      <div className="inicio-contenido">
        <h1>Generador de Políticas Organizativas</h1>
        
        <p className="inicio-descripcion">
          Esta herramienta permite generar políticas organizativas adaptadas al contexto 
          específico de una empresa mediante el uso de modelos de lenguaje ejecutados en local.
        </p>

        <div className="inicio-seccion inicio-seccion-importancia">
          <h2>¿Por qué son importantes las políticas organizativas?</h2>
          <p>
            Las políticas organizativas son fundamentales porque establecen las reglas y 
            directrices que rigen el funcionamiento de una empresa. Ayudan a:
          </p>
          <div className="inicio-grid">
            <div className="inicio-card">
              <span className="inicio-icono">⚖️</span>
              <h3>Cumplimiento legal</h3>
              <p>Evita sanciones y cumple con las normativas</p>
            </div>
            <div className="inicio-card">
              <span className="inicio-icono">🔒</span>
              <h3>Protección de datos</h3>
              <p>Salvaguarda información sensible</p>
            </div>
            <div className="inicio-card">
              <span className="inicio-icono">📋</span>
              <h3>Expectativas claras</h3>
              <p>Todos conocen sus responsabilidades</p>
            </div>
            <div className="inicio-card">
              <span className="inicio-icono">⚠️</span>
              <h3>Reducción de riesgos</h3>
              <p>Minimiza problemas operativos</p>
            </div>
          </div>
        </div>

        <div className="inicio-seccion inicio-seccion-beneficios">
          <h2>Beneficios de tener políticas claras</h2>
          <div className="inicio-grid">
            <div className="inicio-card">
              <span className="inicio-icono">✅</span>
              <h3>Consistencia</h3>
              <p>Todos actúan bajo las mismas reglas</p>
            </div>
            <div className="inicio-card">
              <span className="inicio-icono">💬</span>
              <h3>Transparencia</h3>
              <p>Comunicación clara entre todos</p>
            </div>
            <div className="inicio-card">
              <span className="inicio-icono">🚀</span>
              <h3>Eficiencia</h3>
              <p>Menos tiempo en decisiones</p>
            </div>
            <div className="inicio-card">
              <span className="inicio-icono">💼</span>
              <h3>Profesionalidad</h3>
              <p>Transmite confianza a terceros</p>
            </div>
          </div>
        </div>

        <div className="inicio-seccion inicio-seccion-generar">
          <h2>¿Qué puedes generar?</h2>
          <div className="inicio-lista">
            <div><span>📄</span> Políticas organizativas personalizadas</div>
            <div><span>👍</span> Buenas prácticas recomendadas</div>
            <div><span>🚫</span> Acciones prohibidas</div>
            <div><span>⚠️</span> Identificación de riesgos</div>
          </div>
        </div>

        <div className="inicio-ejemplo-contexto">
          <h3>Ejemplo de contexto</h3>
          <p>
            "Empresa de desarrollo de software que trabaja con datos sensibles 
            de clientes del sector sanitario"
          </p>
        </div>

        <Link to="/generador" className="inicio-boton">
          Prueba el Generador →
        </Link>
      </div>
    </div>
  )
}

export default Inicio