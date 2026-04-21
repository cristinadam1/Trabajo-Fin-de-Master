import { useState } from 'react'
import './MarcoNormativo.css'

function MarcoNormativo() {
  const [normativas, setNormativas] = useState({
    rgpd: false,
    iso27001: false,
    nis2: false
  })

  const toggleNormativa = (key) => {
    setNormativas(prev => ({
      ...prev,
      [key]: !prev[key]
    }))
  }

  return (
    <div className="marco-normativo">
      <div className="marco-normativo-contenido">
        <h1>Marco Normativo y Cumplimiento</h1>
        
        <div className="marco-normativo-introduccion">
          <p>
            Las siguientes normativas son referencias generales sobre requisitos legales y estándares 
            de seguridad de la información. <strong>Esta herramienta no garantiza el cumplimiento 
            automático</strong> de ninguna normativa.
          </p>
          <p>
            Las políticas organizativas generadas deben ser revisadas y adaptadas por profesionales 
            cualificados antes de su implementación. El uso de un LLM local no sustituye el 
            asesoramiento legal o de cumplimiento normativo.
          </p>
        </div>

        <div className="marco-normativa">
          <button 
            className="marco-normativa-boton" 
            onClick={() => toggleNormativa('rgpd')}
          >
            <span className="marco-normativa-icono">
              {normativas.rgpd ? '▼' : '▶'}
            </span>
            RGPD (Reglamento General de Protección de Datos)
          </button>
          
          {normativas.rgpd && (
            <div className="marco-normativa-contenido">
              <div className="marco-normativa-seccion">
                <h3>Descripción</h3>
                <p>
                  El Reglamento General de Protección de Datos (RGPD) es una normativa europea que regula 
                  la protección de datos personales de las personas físicas. Establece principios como 
                  la minimización de datos, la limitación del propósito, la exactitud, la limitación 
                  del plazo de conservación, la integridad y confidencialidad, y la responsabilidad.
                </p>
              </div>

              <div className="marco-normativa-seccion">
                <h3>Relevancia general</h3>
                <p>
                  El RGPD es obligatorio para toda organización que trate datos personales de residentes 
                  en la Unión Europea, con independencia de dónde esté situada la empresa. Las sanciones 
                  por incumplimiento pueden alcanzar hasta 20 millones de euros o el 4% del facturación 
                  global anual.
                </p>
              </div>

              <div className="marco-normativa-seccion">
                <h3>Relación con la aplicación</h3>
                <p>
                  Esta herramienta puede ayudar a generar políticas organizativas que incluyan aspectos 
                  relacionados con el tratamiento de datos personales, como políticas de privacidad, 
                  gestión del consentimiento, derechos de los interesados, medidas de seguridad y 
                  procedimientos de notificación de brechas. Sin embargo, las políticas generadas deben 
                  ser revisadas por un experto en protección de datos.
                </p>
              </div>

              <div className="marco-normativa-enlace">
                <a 
                  href="https://eur-lex.europa.eu/legal-content/ES/TXT/?uri=celex%3A32016R0679" 
                  target="_blank" 
                  rel="noopener noreferrer"
                >
                  Ver normativa completa →
                </a>
              </div>
            </div>
          )}
        </div>

        <div className="marco-normativa">
          <button 
            className="marco-normativa-boton" 
            onClick={() => toggleNormativa('iso27001')}
          >
            <span className="marco-normativa-icono">
              {normativas.iso27001 ? '▼' : '▶'}
            </span>
            ISO 27001 (Seguridad de la Información)
          </button>
          
          {normativas.iso27001 && (
            <div className="marco-normativa-contenido">
              <div className="marco-normativa-seccion">
                <h3>Descripción</h3>
                <p>
                  La ISO 27001 es una norma internacional que especifica los requisitos para establecer, 
                  implementar, mantener y mejorar continuamente un sistema de gestión de seguridad de 
                  la información (SGSI). Proporciona un enfoque sistemática para gestionar la información 
                  sensible de la empresa.
                </p>
              </div>

              <div className="marco-normativa-seccion">
                <h3>Relevancia general</h3>
                <p>
                  ISO 27001 es el estándar más reconocido internacionalmente para la gestión de la 
                  seguridad de la información. Su certificación demuestra a clientes y partes interesadas 
                  que la organización toma en serio la protección de la información.
                </p>
              </div>

              <div className="marco-normativa-seccion">
                <h3>Relación con la aplicación</h3>
                <p>
                  Las políticas generadas pueden incluir controles de seguridad de la información, políticas 
                  de acceso, gestión de activos, seguridad de las comunicaciones y procedimientos de gestión 
                  de incidentes alineados con los requisitos de ISO 27001. La herramienta facilita la 
                  creación de documentación inicial para el SGSI.
                </p>
              </div>

              <div className="marco-normativa-enlace">
                <a 
                  href="https://www.iso.org/standard/27001" 
                  target="_blank" 
                  rel="noopener noreferrer"
                >
                  Ver normativa completa →
                </a>
              </div>
            </div>
          )}
        </div>

        <div className="marco-normativa">
          <button 
            className="marco-normativa-boton" 
            onClick={() => toggleNormativa('nis2')}
          >
            <span className="marco-normativa-icono">
              {normativas.nis2 ? '▼' : '▶'}
            </span>
            NIS2 (Directiva de Seguridad de las Redes)
          </button>
          
          {normativas.nis2 && (
            <div className="marco-normativa-contenido">
              <div className="marco-normativa-seccion">
                <h3>Descripción</h3>
                <p>
                  La Directiva NIS2 (Network and Information Security Directive 2) es una normativa 
                  europea que establece medidas para lograr un nivel común elevado de ciberseguridad 
                  en la Unión Europea. Amplía el ámbito de aplicación de la anterior directiva NIS e 
                  introduce requisitos más estrictos.
                </p>
              </div>

              <div className="marco-normativa-seccion">
                <h3>Relevancia general</h3>
                <p>
                  NIS2 afecta a entidades esenciales e importantes en sectores como energía, transporte, 
                  banca, sanidad, infraestructura digital y administración pública. Las organizaciones 
                  sujetas deben implementar medidas de gestión de riesgos y notificar incidentes.
                </p>
              </div>

              <div className="marco-normativa-seccion">
                <h3>Relación con la aplicación</h3>
                <p>
                  La herramienta puede generar políticas de ciberseguridad, procedimientos de respuesta 
                  ante incidentes, políticas de gestión de riesgos y medidas técnicas y organizativas 
                  que ayuden a las organizaciones sujetas a NIS2 a cumplir con sus obligaciones.
                </p>
              </div>

              <div className="marco-normativa-enlace">
                <a 
                  href="https://eur-lex.europa.eu/legal-content/ES/TXT/?uri=CELEX%3A32022L2555" 
                  target="_blank" 
                  rel="noopener noreferrer"
                >
                  Ver normativa completa →
                </a>
              </div>
            </div>
          )}
        </div>

      </div>
    </div>
  )
}

export default MarcoNormativo
