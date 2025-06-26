# 📁 Gestor de PDFs con FastAPI

Una aplicación web moderna desarrollada con Python y FastAPI para gestionar directorios y archivos PDF de forma organizada y eficiente.

## 🚀 Características

- ✅ **Arquitectura modular** - Backend y frontend completamente separados
- ✅ **API REST completa** - Documentación automática con Swagger/ReDoc
- ✅ **Interfaz moderna** - Frontend responsive con diseño actual
- ✅ **Gestión de directorios** - Crear, listar y eliminar directorios anidados
- ✅ **Subida de archivos** - Drag & drop y validación de archivos PDF
- ✅ **Seguridad** - Validación de rutas y sanitización de archivos
- ✅ **Notificaciones** - Sistema de alertas en tiempo real
- ✅ **Responsive** - Funciona perfectamente en móviles y tablets

## 📋 Requisitos

- Python 3.7+
- pip

## 🏗️ Estructura del Proyecto

```
workplace/
├── app/                          # Backend (FastAPI)
│   ├── __init__.py              # Paquete principal
│   ├── main.py                  # Aplicación principal
│   ├── config.py                # Configuraciones
│   ├── models.py                # Modelos Pydantic
│   ├── services.py              # Lógica de negocio
│   └── api/                     # Rutas de la API
│       ├── __init__.py
│       └── routes.py
├── static/                       # Frontend
│   ├── index.html               # Página principal
│   ├── styles.css               # Estilos CSS
│   └── app.js                   # JavaScript
├── uploads/                      # Archivos subidos (se crea automáticamente)
├── main.py                       # Punto de entrada
├── requirements.txt              # Dependencias
├── README.md                     # Este archivo
└── venv/                         # Entorno virtual
```

## 🛠️ Instalación

1. **Clonar o descargar el proyecto**

2. **Activar el entorno virtual:**
   ```bash
   source venv/bin/activate  # En macOS/Linux
   # o
   venv\Scripts\activate     # En Windows
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

## 🏃‍♂️ Ejecutar la aplicación

### Opción 1: Usando el script principal
```bash
python main.py
```

### Opción 2: Usando uvicorn directamente
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Opción 3: Usando el módulo app
```bash
python -m app.main
```

La aplicación estará disponible en: **http://localhost:8000**

## 📖 Uso

### Interfaz Web

1. **Crear Directorio:** Ingresa la ruta del directorio (ej: `documentos/trabajo/2024`)
2. **Subir PDF:** Selecciona un archivo PDF y especifica el directorio destino
3. **Explorar:** Ve la lista de directorios disponibles con opciones de gestión
4. **Listar Archivos:** Ve los PDFs en cada directorio con información detallada
5. **Descargar/Eliminar:** Acciones directas sobre archivos y directorios

### API REST

#### Endpoints principales:

- `GET /` - Página principal del frontend
- `GET /docs` - Documentación Swagger UI
- `GET /redoc` - Documentación ReDoc
- `GET /api/v1/health` - Estado de la aplicación

#### Gestión de directorios:
```bash
POST /api/v1/directories          # Crear directorio
GET /api/v1/directories           # Listar directorios
GET /api/v1/directories/{path}    # Info de directorio
DELETE /api/v1/directories/{path} # Eliminar directorio
```

#### Gestión de archivos:
```bash
POST /api/v1/files/upload         # Subir archivo PDF
GET /api/v1/files/{path}          # Listar archivos
GET /api/v1/files/download/{path} # Descargar archivo
DELETE /api/v1/files/{path}       # Eliminar archivo
```

## 🔧 Configuración

### Variables de entorno (opcional)

Crea un archivo `.env` en la raíz del proyecto:

```env
# Servidor
HOST=0.0.0.0
PORT=8000
DEBUG=true

# Archivos
UPLOAD_DIR=uploads
MAX_FILE_SIZE=52428800  # 50MB en bytes
ALLOWED_EXTENSIONS=[".pdf"]

# Seguridad
SECRET_KEY=tu-clave-secreta-aqui-cambiala-en-produccion

# Logs
LOG_LEVEL=INFO
```

### Configuración por defecto

- **Puerto:** 8000
- **Host:** 0.0.0.0 (accesible desde cualquier IP)
- **Tamaño máximo de archivo:** 50MB
- **Extensiones permitidas:** Solo PDF
- **Directorio de uploads:** `uploads/`

## 🏗️ Arquitectura

### Backend (FastAPI)

- **`app/main.py`** - Configuración principal de FastAPI
- **`app/config.py`** - Configuraciones centralizadas con Pydantic
- **`app/models.py`** - Modelos de datos para validación
- **`app/services.py`** - Lógica de negocio separada de las rutas
- **`app/api/routes.py`** - Endpoints de la API REST

### Frontend (HTML/CSS/JS)

- **`static/index.html`** - Estructura HTML con diseño moderno
- **`static/styles.css`** - Estilos CSS responsive y animaciones
- **`static/app.js`** - Lógica JavaScript con manejo de errores

## 🔒 Seguridad

- ✅ **Validación de rutas** - Previene ataques de path traversal
- ✅ **Sanitización de archivos** - Nombres de archivo seguros
- ✅ **Validación de tipos** - Solo archivos PDF permitidos
- ✅ **Límites de tamaño** - Control de tamaño de archivos
- ✅ **CORS configurado** - Control de acceso desde otros dominios

## 🚨 Notas de Seguridad

- Esta es una aplicación de desarrollo/demo
- **No incluye autenticación** - Implementa autenticación para producción
- **CORS abierto** - Configura dominios específicos en producción
- **Archivos locales** - Considera usar almacenamiento en la nube para producción

## 🐛 Solución de Problemas

### Error: "Module not found"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Error: "Port already in use"
```bash
# Cambiar puerto en .env o terminar proceso
lsof -ti:8000 | xargs kill -9
```

### Error: "Permission denied"
```bash
# Verificar permisos del directorio
chmod 755 uploads/
```

### Error: "Directory 'static' does not exist"
```bash
# El directorio se crea automáticamente, pero puedes crearlo manualmente
mkdir static
```

## 📝 Desarrollo

### Agregar nuevas funcionalidades

1. **Nuevos endpoints:** Agregar en `app/api/routes.py`
2. **Nueva lógica:** Implementar en `app/services.py`
3. **Nuevos modelos:** Definir en `app/models.py`
4. **Frontend:** Modificar archivos en `static/`

### Estructura de commits recomendada

```
feat: agregar funcionalidad de búsqueda
fix: corregir error en validación de archivos
docs: actualizar documentación de la API
style: mejorar diseño del frontend
refactor: reorganizar estructura de servicios
```

## 📊 Rendimiento

- **FastAPI** - Framework de alto rendimiento
- **Async/await** - Operaciones asíncronas para mejor rendimiento
- **Validación automática** - Pydantic para validación eficiente
- **Archivos estáticos** - Servidos directamente por FastAPI

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🙏 Agradecimientos

- **FastAPI** - Framework web moderno y rápido
- **Pydantic** - Validación de datos
- **Font Awesome** - Iconos
- **Uvicorn** - Servidor ASGI

---

**Desarrollado con ❤️ usando FastAPI y JavaScript moderno** 