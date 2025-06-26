/**
 * Gestor de PDFs - Interfaz Minimalista
 */

class PDFManager {
    constructor() {
        this.currentPath = '';
        this.initializeEventListeners();
        this.loadExplorer();
    }

    initializeEventListeners() {
        // Botones principales
        document.getElementById('newFolderBtn').addEventListener('click', () => this.showFolderModal());
        document.getElementById('uploadBtn').addEventListener('click', () => this.showUploadModal());
        document.getElementById('refreshBtn').addEventListener('click', () => this.loadExplorer());

        // Formularios
        document.getElementById('createDirForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.createDirectory();
        });

        document.getElementById('uploadForm').addEventListener('submit', (e) => {
            console.log('📝 Evento submit del formulario de subida capturado');
            e.preventDefault();
            this.uploadFile();
        });

        // Drag and drop
        this.setupDragAndDrop();
    }

    setupDragAndDrop() {
        const dropZone = document.getElementById('fileDropZone');
        const fileInput = document.getElementById('pdfFile');

        // Hacer clic en el área de arrastrar archivos abre el selector
        dropZone.addEventListener('click', (e) => {
            // Evitar que se active si se hace clic en el input file
            if (e.target !== fileInput) {
                fileInput.click();
            }
        });

        dropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropZone.classList.add('dragover');
        });

        dropZone.addEventListener('dragleave', () => {
            dropZone.classList.remove('dragover');
        });

        dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropZone.classList.remove('dragover');
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                fileInput.files = files;
                this.updateFileLabel(files[0].name);
            }
        });

        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                this.updateFileLabel(e.target.files[0].name);
            }
        });

        // Prevenir que el clic en el input file se propague
        fileInput.addEventListener('click', (e) => {
            e.stopPropagation();
        });
    }

    updateFileLabel(filename) {
        const dropZone = document.getElementById('fileDropZone');
        const fileInput = document.getElementById('pdfFile');
        
        // Actualizar solo la información visual, manteniendo el input file
        const icon = dropZone.querySelector('i');
        const text = dropZone.querySelector('p');
        
        if (icon) {
            icon.className = 'fas fa-file-pdf';
        }
        
        if (text) {
            text.textContent = filename;
        } else {
            // Si no existe el texto, crear uno nuevo
            const newText = document.createElement('p');
            newText.textContent = filename;
            dropZone.appendChild(newText);
        }
        
        // Asegurar que el input file esté presente y funcional
        if (!dropZone.querySelector('#pdfFile')) {
            const newFileInput = document.createElement('input');
            newFileInput.type = 'file';
            newFileInput.id = 'pdfFile';
            newFileInput.name = 'file';
            newFileInput.accept = '.pdf';
            newFileInput.style.display = 'none';
            
            // Restaurar el archivo seleccionado
            if (fileInput && fileInput.files.length > 0) {
                const dt = new DataTransfer();
                dt.items.add(fileInput.files[0]);
                newFileInput.files = dt.files;
            }
            
            dropZone.appendChild(newFileInput);
            
            // Reconfigurar el evento change
            newFileInput.addEventListener('change', (e) => {
                if (e.target.files.length > 0) {
                    this.updateFileLabel(e.target.files[0].name);
                }
            });
            
            // Prevenir propagación del clic
            newFileInput.addEventListener('click', (e) => {
                e.stopPropagation();
            });
        }
    }

    async apiRequest(endpoint, options = {}) {
        try {
            console.log(`🌐 Haciendo petición a: /api/v1${endpoint}`);
            console.log('📋 Opciones:', options);
            
            const response = await fetch(`/api/v1${endpoint}`, {
                headers: {
                    'Accept': 'application/json',
                    ...options.headers
                },
                ...options
            });

            console.log(`📡 Respuesta recibida: ${response.status} ${response.statusText}`);

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                console.error('❌ Error en la respuesta:', errorData);
                
                // Para errores 422, mostrar detalles específicos
                if (response.status === 422) {
                    if (errorData.detail && Array.isArray(errorData.detail)) {
                        const errorMessages = errorData.detail.map(err => 
                            `${err.loc?.join('.')}: ${err.msg}`
                        ).join(', ');
                        throw new Error(`Error de validación: ${errorMessages}`);
                    } else if (errorData.detail) {
                        throw new Error(`Error de validación: ${errorData.detail}`);
                    }
                }
                
                throw new Error(errorData.detail || `Error ${response.status}: ${response.statusText}`);
            }

            // Solo intentar parsear como JSON si el content-type es application/json
            const contentType = response.headers.get('content-type');
            console.log('📄 Content-Type:', contentType);
            
            if (contentType && contentType.includes('application/json')) {
                const jsonResult = await response.json();
                console.log('📄 Respuesta JSON:', jsonResult);
                return jsonResult;
            } else {
                // Para respuestas que no son JSON (como subida de archivos)
                const textResult = await response.text();
                console.log('📄 Respuesta texto:', textResult);
                return textResult;
            }
        } catch (error) {
            console.error('❌ Error en apiRequest:', error);
            throw error;
        }
    }

    showNotification(message, type = 'info') {
        const notifications = document.getElementById('notifications');
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;

        notifications.appendChild(notification);

        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }

    showFolderModal() {
        document.getElementById('folderModal').style.display = 'block';
        
        // Actualizar la información de ubicación
        const locationSpan = document.getElementById('createLocation');
        if (this.currentPath) {
            locationSpan.textContent = this.currentPath;
        } else {
            locationSpan.textContent = 'raíz';
        }
        
        document.getElementById('dirPath').value = '';
        document.getElementById('dirPath').focus();
    }

    showUploadModal() {
        document.getElementById('uploadModal').style.display = 'block';
        
        // Limpiar el contenido anterior
        const dropZone = document.getElementById('fileDropZone');
        dropZone.innerHTML = `
            <i class="fas fa-cloud-upload-alt"></i>
            <p>Arrastra un archivo PDF aquí o haz clic para seleccionar</p>
            <input type="file" id="pdfFile" name="file" accept=".pdf">
        `;
        
        // Reconfigurar el drag and drop después de recrear el contenido
        this.setupDragAndDrop();
    }

    closeModal(modalId) {
        document.getElementById(modalId).style.display = 'none';
    }

    async createDirectory() {
        const dirName = document.getElementById('dirPath').value.trim();
        if (!dirName) {
            this.showNotification('Por favor ingresa un nombre de directorio', 'error');
            return;
        }

        try {
            // Construir la ruta completa del nuevo directorio
            const fullPath = this.currentPath ? `${this.currentPath}/${dirName}` : dirName;
            
            console.log('📁 Creando directorio:', fullPath);
            console.log('📍 Directorio actual:', this.currentPath || 'raíz');
            console.log('📝 Nombre del directorio:', dirName);

            const formData = new FormData();
            formData.append('path', fullPath);

            await this.apiRequest('/directories', {
                method: 'POST',
                body: formData
            });

            this.showNotification(`Directorio '${dirName}' creado exitosamente`, 'success');
            this.closeModal('folderModal');
            this.loadExplorer();
        } catch (error) {
            console.error('❌ Error al crear directorio:', error);
            this.showNotification(error.message, 'error');
        }
    }

    async uploadFile() {
        console.log('🔍 Iniciando subida de archivo...');
        
        const fileInput = document.getElementById('pdfFile');
        console.log('📄 Input file encontrado:', fileInput);
        
        if (!fileInput) {
            console.error('❌ No se encontró el input file');
            this.showNotification('Error: No se pudo acceder al selector de archivos', 'error');
            return;
        }
        
        const file = fileInput.files[0];
        console.log('📄 Archivo seleccionado:', file);

        if (!file) {
            console.log('❌ No hay archivo seleccionado');
            this.showNotification('Por favor selecciona un archivo PDF', 'error');
            return;
        }

        // Validar que es un archivo PDF
        if (!file.name.toLowerCase().endsWith('.pdf')) {
            console.log('❌ El archivo no es un PDF');
            this.showNotification('Por favor selecciona solo archivos PDF', 'error');
            return;
        }

        // Validar tamaño del archivo (máximo 50MB)
        const maxSize = 50 * 1024 * 1024; // 50MB
        if (file.size > maxSize) {
            console.log('❌ El archivo es demasiado grande');
            this.showNotification('El archivo es demasiado grande. Máximo 50MB', 'error');
            return;
        }

        try {
            console.log('📤 Preparando FormData...');
            const formData = new FormData();
            formData.append('file', file);
            formData.append('path', this.currentPath || '');
            
            console.log('📁 Ruta actual:', this.currentPath);
            console.log('📄 Nombre del archivo:', file.name);
            console.log('📏 Tamaño del archivo:', file.size);
            console.log('📄 Tipo MIME del archivo:', file.type);
            
            // Verificar contenido del FormData
            console.log('📋 Contenido del FormData:');
            for (let [key, value] of formData.entries()) {
                console.log(`  ${key}:`, value);
            }

            console.log('🚀 Enviando archivo al servidor...');
            const result = await this.apiRequest('/files/upload', {
                method: 'POST',
                body: formData
            });

            console.log('✅ Respuesta del servidor:', result);
            this.showNotification('Archivo subido exitosamente', 'success');
            this.closeModal('uploadModal');
            this.loadExplorer();
        } catch (error) {
            console.error('❌ Error en la subida:', error);
            this.showNotification(error.message, 'error');
        }
    }

    async loadExplorer() {
        try {
            const [allDirectories, files] = await Promise.all([
                this.apiRequest('/directories'),
                this.currentPath ? this.apiRequest(`/files/${encodeURIComponent(this.currentPath)}`) : []
            ]);

            // Filtrar directorios que pertenecen al directorio actual
            const directories = this.filterDirectoriesForCurrentPath(allDirectories);
            
            this.renderExplorer(directories, files);
        } catch (error) {
            this.showNotification('Error al cargar el explorador', 'error');
        }
    }

    filterDirectoriesForCurrentPath(allDirectories) {
        if (!this.currentPath) {
            // En la raíz, mostrar solo directorios de primer nivel
            return allDirectories.filter(dir => !dir.includes('/'));
        }

        // Para subdirectorios, mostrar solo los que están directamente dentro del directorio actual
        const currentPathPrefix = this.currentPath + '/';
        return allDirectories.filter(dir => {
            // Debe empezar con el prefijo del directorio actual
            if (!dir.startsWith(currentPathPrefix)) {
                return false;
            }
            
            // Debe ser un directorio directo (no un subdirectorio más profundo)
            const relativePath = dir.substring(currentPathPrefix.length);
            return !relativePath.includes('/');
        });
    }

    renderExplorer(directories, files) {
        const dirList = document.getElementById('directoryList');
        const fileList = document.getElementById('fileList');

        // Actualizar breadcrumb dinámico
        this.updateBreadcrumb();

        // Agregar directorio ".." si no estamos en la raíz
        let dirItems = [];
        if (this.currentPath) {
            dirItems.push(`
                <div class="list-item parent-dir" onclick="pdfManager.navigateToParent()">
                    <i class="fas fa-level-up-alt"></i>
                    <span class="name">..</span>
                </div>
            `);
        }

        // Renderizar directorios
        if (directories.length === 0 && !this.currentPath) {
            dirList.innerHTML = '<div class="empty-state">No hay directorios</div>';
        } else {
            const dirElements = directories.map(dir => `
                <div class="list-item" onclick="pdfManager.navigateTo('${dir}')">
                    <i class="fas fa-folder"></i>
                    <span class="name">${dir}</span>
                    <div class="actions">
                        <button class="action-icon delete" onclick="event.stopPropagation(); pdfManager.deleteDirectory('${dir}')" title="Eliminar">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
            `).join('');
            
            dirList.innerHTML = dirItems.join('') + dirElements;
        }

        // Renderizar archivos con indentación
        if (files.length === 0) {
            fileList.innerHTML = '<div class="empty-state">No hay archivos PDF</div>';
        } else {
            fileList.innerHTML = files.map(file => `
                <div class="list-item file-item">
                    <i class="fas fa-file-pdf"></i>
                    <span class="name">${file.name}</span>
                    <div class="actions">
                        <button class="action-icon" onclick="pdfManager.downloadFile('${file.path}')" title="Descargar">
                            <i class="fas fa-download"></i>
                        </button>
                        <button class="action-icon delete" onclick="pdfManager.deleteFile('${file.path}')" title="Eliminar">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
            `).join('');
        }
    }

    updateBreadcrumb() {
        const breadcrumbPath = document.getElementById('breadcrumbPath');
        
        if (!this.currentPath) {
            breadcrumbPath.innerHTML = `
                <span class="breadcrumb-item active">
                    <i class="fas fa-home"></i> Inicio
                </span>
            `;
            return;
        }

        const pathParts = this.currentPath.split('/').filter(part => part);
        let breadcrumbHTML = `
            <span class="breadcrumb-item" onclick="pdfManager.navigateTo('')">
                <i class="fas fa-home"></i> Inicio
            </span>
        `;

        let currentPath = '';
        pathParts.forEach((part, index) => {
            currentPath += (currentPath ? '/' : '') + part;
            const isLast = index === pathParts.length - 1;
            
            breadcrumbHTML += `
                <span class="breadcrumb-separator">
                    <i class="fas fa-chevron-right"></i>
                </span>
                <span class="breadcrumb-item ${isLast ? 'active' : ''}" 
                      ${!isLast ? `onclick="pdfManager.navigateTo('${currentPath}')"` : ''}>
                    ${part}
                </span>
            `;
        });

        breadcrumbPath.innerHTML = breadcrumbHTML;
    }

    navigateTo(path) {
        this.currentPath = path;
        this.loadExplorer();
    }

    async downloadFile(path) {
        try {
            console.log(`🔍 Intentando descargar: ${path}`);
            
            // Crear un enlace temporal para la descarga
            const link = document.createElement('a');
            link.href = `/api/v1/files/download/${encodeURIComponent(path)}`;
            link.download = path.split('/').pop(); // Obtener solo el nombre del archivo
            link.target = '_blank';
            
            // Añadir el enlace al DOM temporalmente
            document.body.appendChild(link);
            
            // Hacer clic en el enlace
            link.click();
            
            // Remover el enlace del DOM
            document.body.removeChild(link);
            
            this.showNotification('Descarga iniciada', 'success');
        } catch (error) {
            console.error('Error al descargar:', error);
            this.showNotification(`Error al descargar: ${error.message}`, 'error');
        }
    }

    async deleteFile(path) {
        if (!await this.confirm('¿Eliminar este archivo?')) return;

        try {
            await this.apiRequest(`/files/${encodeURIComponent(path)}`, {
                method: 'DELETE'
            });
            this.showNotification('Archivo eliminado', 'success');
            this.loadExplorer();
        } catch (error) {
            this.showNotification(error.message, 'error');
        }
    }

    async deleteDirectory(path) {
        if (!await this.confirm('¿Eliminar este directorio y todo su contenido?')) return;

        try {
            await this.apiRequest(`/directories/${encodeURIComponent(path)}`, {
                method: 'DELETE'
            });
            this.showNotification('Directorio eliminado', 'success');
            this.loadExplorer();
        } catch (error) {
            this.showNotification(error.message, 'error');
        }
    }

    async confirm(message) {
        return new Promise((resolve) => {
            const modal = document.getElementById('confirmModal');
            document.getElementById('confirmMessage').textContent = message;
            modal.style.display = 'block';

            const handleConfirm = () => {
                modal.style.display = 'none';
                cleanup();
                resolve(true);
            };

            const handleCancel = () => {
                modal.style.display = 'none';
                cleanup();
                resolve(false);
            };

            const cleanup = () => {
                document.getElementById('confirmOk').removeEventListener('click', handleConfirm);
                document.getElementById('confirmCancel').removeEventListener('click', handleCancel);
            };

            document.getElementById('confirmOk').addEventListener('click', handleConfirm);
            document.getElementById('confirmCancel').addEventListener('click', handleCancel);
        });
    }

    navigateToParent() {
        if (!this.currentPath) return;
        
        const pathParts = this.currentPath.split('/').filter(part => part);
        pathParts.pop(); // Remover el último directorio
        this.currentPath = pathParts.join('/');
        this.loadExplorer();
    }
}

// Funciones globales
window.closeModal = (modalId) => {
    document.getElementById(modalId).style.display = 'none';
};

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    window.pdfManager = new PDFManager();
}); 
window.listFiles = () => window.pdfManager.listFiles(); 