# Generador de Políticas Organizativas

Aplicación web para generar políticas organizativas, guías de actuación, buenas prácticas, acciones prohibidas, identificación de riesgos y explicaciones justificativas mediante un modelo de lenguaje (LLM).

## Requisitos

- Docker Desktop
- Docker Compose
- Acceso a un servidor LLM externo (Ollama, OpenAI, etc.)

##Inicio

### 1. Configuración del LLM

Crear un archivo `.env` en la raíz del proyecto:

```env
# Servidor LLM
LLM_API_URL=http://localhost:11434/api/generate
LLM_API_KEY=
LLM_MODEL=llama3
```

Para OllAMA:
- URL: `http://localhost:11434/api/generate`
- Modelo: `llama3` (o el que tengas descargado)

Para OpenAI:
- URL: `https://api.openai.com/v1/chat/completions`
- API Key: Tu clave de API

### 2. Arrancar la aplicación

```bash
docker compose up -d
```

### 3. Acceder

- Frontend: http://localhost:3000
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Uso

1. Abre http://localhost:3000
2. Escribe un contexto organizativo en el formulario
3. Haz clic en "Generar Políticas"
4. Visualiza los resultados generados
5. Guarda en favoritos si lo deseas
6. Consulta el historial en "Historial"

## Estructura del Proyecto

```
.
├── docker-compose.yml    # Orquestación de contenedores
├── backend/              # API FastAPI
│   ├── app/
│   │   ├── main.py       # Aplicación principal
│   │   ├── models.py    # Modelos de datos
│   │   ├── schemas.py   # Esquemas validación
│   │   ├── database.py # Conexión PostgreSQL
│   │   ├── routers/    # Endpoints API
│   │   └── services/   # Lógica de negocio
├── frontend/             # Aplicación React
│   ├── src/
│   │   ├── components/  # Componentes React
│   │   ├── App.jsx     # Componente principal
│   │   └── App.css     # Estilos
│   └── package.json
└── SPEC.md              # Especificación del proyecto
```

## Comandos útiles

```bash
# Ver contenedores
docker compose ps

# Ver logs
docker compose logs -f

# Parar contenedores
docker compose down

# Reconstruir contenedores
docker compose build --no-cache

# Ejecutar pruebas
docker compose exec backend pytest
```

## API Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | /api/generate | Generar contenido |
| GET | /api/generations | Listar historial |
| GET | /api/generations/{id} | Ver generación |
| DELETE | /api/generations/{id} | Eliminar |
| PUT | /api/generations/{id}/favorite | Marcar favorito |
| POST | /api/regenerate/{id} | Regenerar |

## Tecnologías

- Frontend: React + Vite
- Backend: FastAPI (Python)
- Base de datos: PostgreSQL
- Contenedores: Docker Compose

## Desarrollo

### Desarrollo local sin Docker

```bash
# Frontend
cd frontend && npm install && npm run dev

# Backend
cd backend && pip install -r requirements.txt && uvicorn app.main:app --reload
```

## Licencia

MIT