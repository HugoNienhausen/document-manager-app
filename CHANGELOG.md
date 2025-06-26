# Changelog

Todas las notables mejoras y cambios en este proyecto serán documentadas en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 26/06/2025

### Añadido
- 🏗️ **Arquitectura modular del frontend**
  - Reorganización de JavaScript en módulos ES6
  - Separación de CSS en archivos modulares por funcionalidad
  - Mejor organización del código con separación de responsabilidades
  - Documentación de la estructura modular

### Mejorado
- 📁 **Funcionalidad de expansión de directorios**
  - Los directorios expandidos ahora muestran subdirectorios y archivos
  - Soporte para expansión anidada de subdirectorios
  - Mejor experiencia de navegación sin perder contexto
  - Nuevo método `filterDirectoriesForPath` para expansión

- 🍞 **Breadcrumb horizontal**
  - Cambio de layout vertical a horizontal
  - Mejor integración visual con la interfaz
  - Scroll horizontal cuando el path es muy largo
  - Corrección de clase CSS para consistencia

- 🔙 **Botón de directorio padre**
  - Diseño minimalista con texto ".."
  - Estilos discretos que se integran mejor con la interfaz
  - Icono de flecha hacia arriba más intuitivo
  - Efectos hover sutiles

### Corregido
- 🔧 **Renderizado de contenido de directorios**
  - Método `renderDirectoryContent` actualizado para manejar subdirectorios
  - Corrección de parámetros para mostrar tanto directorios como archivos
  - Mejor manejo de estados vacíos en directorios expandidos

---

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
├── static/                # Frontend modular
│   ├── index.html        # Interfaz principal
│   ├── css/              # CSS modular
│   ├── js/               # JavaScript modular
│   └── README.md         # Documentación frontend
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