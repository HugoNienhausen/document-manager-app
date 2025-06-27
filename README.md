# Document Manager App

Una aplicación web moderna para la gestión de documentos PDF con metadatos, construida con FastAPI y JavaScript modular.

## 🚀 Características

- **Gestión de directorios**: Crear, navegar y eliminar directorios
- **Subida de documentos**: Subir archivos PDF con metadatos completos
- **Base de datos PostgreSQL**: Almacenamiento persistente con SQLAlchemy
- **Interfaz modular**: Frontend JavaScript organizado en módulos
- **API RESTful**: Backend FastAPI con documentación automática
- **Validación de archivos**: Verificación de tipos y tamaños
- **Sistema de metadatos**: Categorización por tipo, cliente y categoría
- **Hash de archivos**: Detección de duplicados por contenido

## 🛠️ Tecnologías

### Backend
- **FastAPI**: Framework web moderno y rápido
- **PostgreSQL**: Base de datos relacional
- **SQLAlchemy**: ORM para Python
- **Pydantic**: Validación de datos
- **Uvicorn**: Servidor ASGI

### Frontend
- **JavaScript ES6+**: Código modular y moderno
- **CSS3**: Estilos responsivos y modernos
- **HTML5**: Estructura semántica

## 📦 Instalación

### Prerrequisitos
- Python 3.11+
- PostgreSQL
- Node.js (opcional, para desarrollo)

### 1. Clonar el repositorio
```bash
git clone https://github.com/HugoNienhausen/document-manager-app.git
cd document-manager-app
```

### 2. Configurar entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar base de datos
```bash
# Crear base de datos PostgreSQL
createdb document_manager

# Configurar variables de entorno
cp config.env.example config.env
# Editar config.env con tus credenciales de base de datos
```

### 5. Inicializar base de datos
```bash
python scripts/init_database.py
```

### 6. Ejecutar la aplicación
```bash
python main.py
```

La aplicación estará disponible en:
- **Frontend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📁 Estructura del proyecto

```
document-manager-app/
├── app/                    # Backend FastAPI
│   ├── api/               # Rutas de la API
│   ├── models/            # Modelos SQLAlchemy
│   ├── config.py          # Configuración
│   ├── database.py        # Conexión a base de datos
│   ├── main.py           # Aplicación principal
│   ├── pydantic_models.py # Modelos Pydantic
│   └── services.py       # Lógica de negocio
├── static/                # Frontend
│   ├── css/              # Estilos CSS
│   ├── js/               # JavaScript modular
│   │   └── modules/      # Módulos JS
│   └── index.html        # Página principal
├── scripts/              # Scripts de utilidad
├── uploads/              # Archivos subidos
├── docs/                 # Documentación
└── requirements.txt      # Dependencias Python
```

## 🔧 Configuración

### Variables de entorno
Crea un archivo `config.env` con las siguientes variables:

```env
DATABASE_URL=postgresql://usuario:password@localhost/document_manager
SECRET_KEY=tu_clave_secreta_aqui
ALLOWED_EXTENSIONS=pdf
MAX_FILE_SIZE=10485760
UPLOAD_PATH=uploads
```

### Base de datos
La aplicación utiliza PostgreSQL con las siguientes tablas:
- `documents`: Documentos subidos
- `document_types`: Tipos de documento
- `categories`: Categorías
- `clients`: Clientes

## 📚 API Endpoints

### Directorios
- `GET /api/v1/directories` - Listar directorios
- `POST /api/v1/directories` - Crear directorio
- `DELETE /api/v1/directories/{path}` - Eliminar directorio

### Archivos
- `GET /api/v1/files/{path}` - Listar archivos
- `POST /api/v1/files/upload` - Subir archivo
- `GET /api/v1/files/download/{path}` - Descargar archivo
- `DELETE /api/v1/files/{path}` - Eliminar archivo

### Documentos con metadatos
- `POST /api/v1/documents/upload` - Subir documento con metadatos
- `GET /api/v1/documents/types` - Obtener tipos de documento
- `GET /api/v1/documents/categories` - Obtener categorías
- `GET /api/v1/documents/clients` - Obtener clientes

## 🎯 Funcionalidades principales

### Gestión de directorios
- Navegación visual con breadcrumb
- Creación de directorios anidados
- Eliminación recursiva de directorios

### Subida de documentos
- Interfaz drag & drop
- Validación de tipos de archivo
- Metadatos obligatorios (tipo, categoría)
- Metadatos opcionales (cliente)
- Detección de duplicados por hash

### Explorador de archivos
- Vista de lista con detalles
- Acciones de descarga y eliminación
- Navegación entre directorios
- Información de archivos

## 🔒 Seguridad

- Validación de rutas para prevenir path traversal
- Sanitización de nombres de archivo
- Límites de tamaño de archivo
- Verificación de tipos de archivo permitidos
- Hash SHA-256 para detección de duplicados

## 🧪 Desarrollo

### Ejecutar en modo desarrollo
```bash
python main.py
```

### Estructura modular del frontend
- `app.js`: Aplicación principal
- `modules/api.js`: Comunicación con la API
- `modules/fileManager.js`: Gestión de archivos
- `modules/documentManager.js`: Gestión de documentos
- `modules/ui.js`: Interfaz de usuario
- `modules/renderer.js`: Renderizado de contenido
- `modules/validation.js`: Validaciones

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👨‍💻 Autor

**Hugo Nienhausen**
- GitHub: [@HugoNienhausen](https://github.com/HugoNienhausen)
- Ubicación: Barcelona, Spain

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request.

## 📄 Changelog

Ver [CHANGELOG.md](CHANGELOG.md) para el historial de cambios. 