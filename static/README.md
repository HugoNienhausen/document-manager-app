# Frontend Modular - PDF Manager

## Estructura de Archivos

### JavaScript Modular

```
static/js/
├── app.js                    # Aplicación principal
└── modules/
    ├── api.js               # Servicio de API
    ├── validation.js        # Validación de archivos y formularios
    ├── ui.js                # Gestión de UI (modales, notificaciones)
    ├── renderer.js          # Renderizado de elementos
    └── fileManager.js       # Gestión de archivos y directorios
```

### CSS Modular

```
static/css/
├── main.css                 # Archivo principal que importa todos los módulos
├── base.css                 # Reset y configuración base
├── header.css               # Header y navegación
├── actions.css              # Panel de acciones y botones
├── explorer.css             # Explorador de archivos
├── modals.css               # Modales y formularios
└── notifications.css        # Notificaciones y animaciones
```

## Módulos JavaScript

### 1. API Service (`modules/api.js`)
- Maneja todas las peticiones al backend
- Métodos para directorios, archivos y salud
- Manejo centralizado de errores

### 2. Validation Service (`modules/validation.js`)
- Validación de archivos PDF
- Validación de nombres de directorios
- Sanitización de nombres de archivos
- Formateo de tamaños de archivo

### 3. UI Service (`modules/ui.js`)
- Gestión de modales
- Sistema de notificaciones
- Drag and drop de archivos
- Diálogos de confirmación
- Actualización de breadcrumb

### 4. Renderer Service (`modules/renderer.js`)
- Renderizado del explorador
- Renderizado de contenido de directorios
- Estados de carga y vacío
- Expansión/colapso de directorios

### 5. File Manager Service (`modules/fileManager.js`)
- Gestión de archivos (subir, descargar, eliminar)
- Gestión de directorios (crear, eliminar)
- Navegación entre directorios
- Carga del explorador

## Módulos CSS

### 1. Base (`base.css`)
- Reset CSS
- Configuración general
- Utilidades básicas
- Responsive base

### 2. Header (`header.css`)
- Estilos del header
- Breadcrumb de navegación
- Títulos y subtítulos

### 3. Actions (`actions.css`)
- Panel de acciones
- Botones principales
- Botones de icono
- Estados hover

### 4. Explorer (`explorer.css`)
- Explorador de archivos
- Lista de directorios y archivos
- Estados expandido/colapsado
- Iconos y acciones

### 5. Modals (`modals.css`)
- Modales base
- Formularios
- Zona de drag and drop
- Diálogos de confirmación

### 6. Notifications (`notifications.css`)
- Sistema de notificaciones
- Animaciones de entrada/salida
- Tipos de notificación (success, error, info)

## Ventajas de la Estructura Modular

### JavaScript
- **Separación de responsabilidades**: Cada módulo tiene una función específica
- **Mantenibilidad**: Fácil de mantener y actualizar
- **Reutilización**: Los módulos pueden reutilizarse en otras partes
- **Testabilidad**: Cada módulo puede testearse independientemente
- **Escalabilidad**: Fácil agregar nuevas funcionalidades

### CSS
- **Organización**: Estilos organizados por funcionalidad
- **Mantenimiento**: Fácil encontrar y modificar estilos específicos
- **Reutilización**: Módulos CSS pueden reutilizarse
- **Performance**: Solo se cargan los estilos necesarios
- **Colaboración**: Múltiples desarrolladores pueden trabajar en diferentes módulos

## Uso

### Importación de Módulos
```javascript
import { apiService } from './modules/api.js';
import { validationService } from './modules/validation.js';
import { uiService } from './modules/ui.js';
import { rendererService } from './modules/renderer.js';
import { fileManagerService } from './modules/fileManager.js';
```

### Uso de Servicios
```javascript
// API
const directories = await apiService.getDirectories();

// Validación
const validation = validationService.validatePdfFile(file);

// UI
uiService.showNotification('Mensaje', 'success');

// Renderizado
rendererService.renderExplorer(directories, files);

// Gestión de archivos
await fileManagerService.uploadFile();
```

## Compatibilidad

La aplicación mantiene la misma funcionalidad que la versión anterior, pero con una estructura más organizada y mantenible. Todos los métodos públicos están disponibles a través de la instancia global `pdfManager`.

## Próximos Pasos

1. **Testing**: Implementar tests unitarios para cada módulo
2. **Documentación**: Generar documentación automática con JSDoc
3. **Optimización**: Implementar lazy loading de módulos
4. **TypeScript**: Migrar a TypeScript para mejor tipado
5. **Bundling**: Implementar un bundler como Webpack o Vite 