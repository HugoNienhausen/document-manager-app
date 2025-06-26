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
        dropZone.addEventListener('click', () => {
            fileInput.click();
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
    }

    updateFileLabel(filename) {
        const dropZone = document.getElementById('fileDropZone');
        dropZone.innerHTML = `
            <i class="fas fa-file-pdf"></i>
            <p>${filename}</p>
        `;
    }

    async apiRequest(endpoint, options = {}) {
        try {
            const response = await fetch(`/api/v1${endpoint}`, {
                headers: {
                    'Accept': 'application/json',
                    ...options.headers
                },
                ...options
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || `Error ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
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
        document.getElementById('dirPath').value = this.currentPath;
        document.getElementById('dirPath').focus();
    }

    showUploadModal() {
        document.getElementById('uploadModal').style.display = 'block';
        document.getElementById('fileDropZone').innerHTML = `
            <i class="fas fa-cloud-upload-alt"></i>
            <p>Arrastra un archivo PDF aquí o haz clic para seleccionar</p>
        `;
    }

    closeModal(modalId) {
        document.getElementById(modalId).style.display = 'none';
    }

    async createDirectory() {
        const path = document.getElementById('dirPath').value.trim();
        if (!path) {
            this.showNotification('Por favor ingresa un nombre de directorio', 'error');
            return;
        }

        try {
            const formData = new FormData();
            formData.append('path', path);

            await this.apiRequest('/directories', {
                method: 'POST',
                body: formData
            });

            this.showNotification('Directorio creado exitosamente', 'success');
            this.closeModal('folderModal');
            this.loadExplorer();
        } catch (error) {
            this.showNotification(error.message, 'error');
        }
    }

    async uploadFile() {
        const fileInput = document.getElementById('pdfFile');
        const file = fileInput.files[0];

        if (!file) {
            this.showNotification('Por favor selecciona un archivo PDF', 'error');
            return;
        }

        try {
            const formData = new FormData();
            formData.append('file', file);
            formData.append('path', this.currentPath || '');

            await this.apiRequest('/files/upload', {
                method: 'POST',
                body: formData
            });

            this.showNotification('Archivo subido exitosamente', 'success');
            this.closeModal('uploadModal');
            this.loadExplorer();
        } catch (error) {
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
            window.open(`/api/v1/files/download/${encodeURIComponent(path)}`, '_blank');
            this.showNotification('Descarga iniciada', 'success');
        } catch (error) {
            this.showNotification('Error al descargar', 'error');
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