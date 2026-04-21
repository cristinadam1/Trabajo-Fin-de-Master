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

        <div className="inicio-seccion">
          <h2>¿Por qué son importantes las políticas organizativas?</h2>
          <p>
            Las políticas organizativas son fundamentales porque establecen las reglas y 
            directrices que rigen el funcionamiento de una empresa. Ayudan a:
          </p>
          <ul>
            <li><strong>Garantizar el cumplimiento legal</strong> y evitar sanciones</li>
            <li><strong>Proteger los datos</strong> de clientes y empleados</li>
            <li><strong>Establecer expectativas claras</strong> para todos los miembros de la organización</li>
            <li><strong>Reducir riesgos</strong> operativos y de seguridad</li>
            <li><strong>Mejorar la comunicación</strong> interna y externa</li>
          </ul>
        </div>

        <div className="inicio-seccion">
          <h2>Beneficios de tener políticas claras</h2>
          <ul>
            <li><strong>Consistencia:</strong> Todos actúan bajo las mismas reglas</li>
            <li><strong>Transparencia:</strong> Los empleados conocen sus responsabilidades</li>
            <li><strong>Protección:</strong> Se reducen riesgos legales y operativos</li>
            <li><strong>Eficiencia:</strong> Menos tiempo tomando decisiones</li>
            <li><strong>Profesionalidad:</strong> La empresa transmite confianza</li>
          </ul>
        </div>

        <div className="inicio-seccion">
          <h2>¿Qué puedes generar?</h2>
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
