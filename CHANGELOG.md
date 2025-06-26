# Changelog

Todas las notables mejoras y cambios en este proyecto serán documentadas en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 26/06/2025

### Mejorado
- 🎨 **Estructura visual de directorios expandibles**
  - Contenido expandible ahora se muestra debajo del header del directorio
  - Mejor jerarquía visual similar al Finder de Apple
  - Eliminación de alineación horizontal que causaba confusión
  - Cambio de `flex-direction` a `column` para mejor organización

### Corregido
- 🔧 **Alineación de elementos en directorios expandibles**
  - Eliminado `align-items: center` que causaba que el contenido se mostrara al lado
  - Mejorada la estructura CSS para presentación vertical clara

---

## [1.0.0] - 26/06/2025

### Añadido
- 🎉 **Versión inicial** del Gestor de PDFs
- **Backend completo** con FastAPI y arquitectura modular
- **Frontend minimalista** con interfaz moderna y responsive
- **Navegación visual** con breadcrumb dinámico
- **Subida de archivos** con drag & drop y click
- **Gestión de directorios** con creación y eliminación
- **Navegación por directorios** con botón ".." para volver atrás
- **Indentación visual** de archivos PDF para mostrar jerarquía
- **Interfaz responsive** que funciona en móviles y desktop
- **Notificaciones** en tiempo real para feedback del usuario
- **Documentación completa** con docstrings y README

### Características Técnicas
- Arquitectura modular con separación de responsabilidades
- API REST completa con documentación automática
- Validación de archivos y rutas seguras
- Manejo de errores robusto
- Configuración flexible con variables de entorno
- Código limpio y bien documentado

### Estructura del Proyecto
```
workplace/
├── app/                    # Backend modular
│   ├── api/               # Rutas de la API
│   ├── config.py          # Configuración
│   ├── models.py          # Modelos de datos
│   ├── services.py        # Lógica de negocio
│   └── main.py           # Aplicación FastAPI
├── static/                # Frontend
│   ├── index.html        # Interfaz principal
│   ├── styles.css        # Estilos
│   └── app.js           # JavaScript
├── uploads/              # Archivos subidos
├── requirements.txt      # Dependencias
└── README.md            # Documentación
```

---

## Convenciones de Versionado

- **MAJOR.MINOR.PATCH** (ej: 1.0.0)
- **MAJOR**: Cambios incompatibles con versiones anteriores
- **MINOR**: Nuevas funcionalidades compatibles
- **PATCH**: Correcciones de bugs compatibles

## Tipos de Cambios

- **Añadido**: Nuevas funcionalidades
- **Cambiado**: Cambios en funcionalidades existentes
- **Deprecado**: Funcionalidades que serán removidas
- **Removido**: Funcionalidades eliminadas
- **Corregido**: Correcciones de bugs
- **Seguridad**: Mejoras de seguridad 