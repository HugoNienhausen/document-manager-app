/**
 * PDF Manager - Frontend Application
 */

class PDFManager {
    constructor() {
        this.currentPath = '';
        this.initializeEventListeners();
        this.loadExplorer();
    }

    initializeEventListeners() {
        // Main buttons
        document.getElementById('newFolderBtn').addEventListener('click', () => this.showFolderModal());
        document.getElementById('uploadBtn').addEventListener('click', () => this.showUploadModal());
        document.getElementById('refreshBtn').addEventListener('click', () => this.loadExplorer());

        // Forms
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

        // Click on drop zone opens file selector
        dropZone.addEventListener('click', (e) => {
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

        // Prevent click propagation on file input
        fileInput.addEventListener('click', (e) => {
            e.stopPropagation();
        });
    }

    updateFileLabel(filename) {
        const dropZone = document.getElementById('fileDropZone');
        const fileInput = document.getElementById('pdfFile');
        
        // Update visual information
        const icon = dropZone.querySelector('i');
        const text = dropZone.querySelector('p');
        
        if (icon) {
            icon.className = 'fas fa-file-pdf';
        }
        
        if (text) {
            text.textContent = filename;
        } else {
            const newText = document.createElement('p');
            newText.textContent = filename;
            dropZone.appendChild(newText);
        }
        
        // Ensure file input is present and functional
        if (!dropZone.querySelector('#pdfFile')) {
            const newFileInput = document.createElement('input');
            newFileInput.type = 'file';
            newFileInput.id = 'pdfFile';
            newFileInput.name = 'file';
            newFileInput.accept = '.pdf';
            newFileInput.style.display = 'none';
            
            // Restore selected file
            if (fileInput && fileInput.files.length > 0) {
                const dt = new DataTransfer();
                dt.items.add(fileInput.files[0]);
                newFileInput.files = dt.files;
            }
            
            dropZone.appendChild(newFileInput);
            
            // Reconfigure change event
            newFileInput.addEventListener('change', (e) => {
                if (e.target.files.length > 0) {
                    this.updateFileLabel(e.target.files[0].name);
                }
            });
            
            // Prevent click propagation
            newFileInput.addEventListener('click', (e) => {
                e.stopPropagation();
            });
        }
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
                
                // Handle validation errors
                if (response.status === 422) {
                    if (errorData.detail && Array.isArray(errorData.detail)) {
                        const errorMessages = errorData.detail.map(err => 
                            `${err.loc?.join('.')}: ${err.msg}`
                        ).join(', ');
                        throw new Error(`Validation error: ${errorMessages}`);
                    } else if (errorData.detail) {
                        throw new Error(`Validation error: ${errorData.detail}`);
                    }
                }
                
                throw new Error(errorData.detail || `Error ${response.status}: ${response.statusText}`);
            }

            // Parse response based on content type
            const contentType = response.headers.get('content-type');
            
            if (contentType && contentType.includes('application/json')) {
                return await response.json();
            } else {
                return await response.text();
            }
        } catch (error) {
            console.error('API request error:', error);
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
        
        // Update modal info
        const modalInfo = document.getElementById('modalInfo');
        const location = this.currentPath ? `en "${this.currentPath}"` : 'en la raíz';
        modalInfo.innerHTML = `
            <p><i class="fas fa-info-circle"></i> El directorio se creará <span>${location}</span></p>
        `;
    }

    showUploadModal() {
        document.getElementById('uploadModal').style.display = 'block';
        
        // Clear previous content
        const dropZone = document.getElementById('fileDropZone');
        dropZone.innerHTML = `
            <i class="fas fa-cloud-upload-alt"></i>
            <p>Arrastra un archivo PDF aquí o haz clic para seleccionar</p>
            <input type="file" id="pdfFile" name="file" accept=".pdf">
        `;
        
        // Reconfigure drag and drop
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
            // Build full path for new directory
            const fullPath = this.currentPath ? `${this.currentPath}/${dirName}` : dirName;

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
            console.error('Error creating directory:', error);
            this.showNotification(error.message, 'error');
        }
    }

    async uploadFile() {
        const fileInput = document.getElementById('pdfFile');
        
        if (!fileInput) {
            this.showNotification('Error: No se pudo acceder al selector de archivos', 'error');
            return;
        }
        
        const file = fileInput.files[0];

        if (!file) {
            this.showNotification('Por favor selecciona un archivo PDF', 'error');
            return;
        }

        // Validate PDF file
        if (!file.name.toLowerCase().endsWith('.pdf')) {
            this.showNotification('Por favor selecciona solo archivos PDF', 'error');
            return;
        }

        // Validate file size (max 50MB)
        const maxSize = 50 * 1024 * 1024;
        if (file.size > maxSize) {
            this.showNotification('El archivo es demasiado grande. Máximo 50MB', 'error');
            return;
        }

        try {
            const formData = new FormData();
            formData.append('file', file);
            formData.append('path', this.currentPath || '');

            const result = await this.apiRequest('/files/upload', {
                method: 'POST',
                body: formData
            });

            this.showNotification('Archivo subido exitosamente', 'success');
            this.closeModal('uploadModal');
            this.loadExplorer();
        } catch (error) {
            console.error('Upload error:', error);
            this.showNotification(error.message, 'error');
        }
    }

    async loadExplorer() {
        try {
            const [allDirectories, files] = await Promise.all([
                this.apiRequest('/directories'),
                this.currentPath ? this.apiRequest(`/files/${encodeURIComponent(this.currentPath)}`) : []
            ]);

            // Filter directories for current path
            const directories = this.filterDirectoriesForCurrentPath(allDirectories);
            
            this.renderExplorer(directories, files);
        } catch (error) {
            this.showNotification('Error al cargar el explorador', 'error');
        }
    }

    filterDirectoriesForCurrentPath(allDirectories) {
        if (!this.currentPath) {
            // Root level - show only first level directories
            return allDirectories.filter(dir => !dir.includes('/'));
        }

        // Subdirectories - show only direct children
        const currentPathPrefix = this.currentPath + '/';
        return allDirectories.filter(dir => {
            if (!dir.startsWith(currentPathPrefix)) {
                return false;
            }
            
            const relativePath = dir.substring(currentPathPrefix.length);
            return !relativePath.includes('/');
        });
    }

    renderExplorer(directories, files) {
        const explorerList = document.getElementById('explorerList');

        // Update breadcrumb
        this.updateBreadcrumb();

        // Add parent directory ".." if not in root
        let explorerHTML = '';
        if (this.currentPath) {
            explorerHTML += `
                <div class="explorer-item parent-dir" onclick="pdfManager.navigateToParent()">
                    <div class="directory-header">
                        <div class="directory-icon">
                            <i class="fas fa-level-up-alt"></i>
                        </div>
                        <span class="item-name">..</span>
                    </div>
                </div>
            `;
        }

        // Render directories with expandable functionality
        if (directories.length === 0 && !this.currentPath) {
            explorerHTML += '<div class="empty-state">No hay directorios</div>';
        } else {
            directories.forEach(dir => {
                const dirName = dir.split('/').pop();
                explorerHTML += `
                    <div class="explorer-item directory" data-path="${dir}">
                        <div class="directory-header">
                            <div class="directory-toggle" onclick="event.stopPropagation(); pdfManager.toggleDirectory('${dir}')">
                                <i class="fas fa-chevron-right"></i>
                            </div>
                            <div class="directory-icon">
                                <i class="fas fa-folder"></i>
                            </div>
                            <span class="item-name" onclick="pdfManager.navigateTo('${dir}')">${dirName}</span>
                            <div class="item-actions">
                                <button class="action-icon delete" onclick="event.stopPropagation(); pdfManager.deleteDirectory('${dir}')" title="Eliminar">
                                    <i class="fas fa-trash"></i>
                                </button>
                            </div>
                        </div>
                        <div class="directory-content" id="content-${dir.replace(/[^a-zA-Z0-9]/g, '-')}">
                            <div class="loading">Cargando...</div>
                        </div>
                    </div>
                `;
            });
        }

        // Render files in current directory
        if (files.length > 0) {
            files.forEach(file => {
                explorerHTML += `
                    <div class="explorer-item file">
                        <div class="directory-header">
                            <div class="directory-icon"></div>
                            <div class="file-icon">
                                <i class="fas fa-file-pdf"></i>
                            </div>
                            <span class="item-name">${file.name}</span>
                            <div class="item-actions">
                                <button class="action-icon" onclick="pdfManager.downloadFile('${file.path}')" title="Descargar">
                                    <i class="fas fa-download"></i>
                                </button>
                                <button class="action-icon delete" onclick="pdfManager.deleteFile('${file.path}')" title="Eliminar">
                                    <i class="fas fa-trash"></i>
                                </button>
                            </div>
                        </div>
                    </div>
                `;
            });
        } else if (!this.currentPath && directories.length === 0) {
            explorerHTML += '<div class="empty-state">No hay archivos PDF</div>';
        }

        explorerList.innerHTML = explorerHTML;
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
            // Create temporary download link
            const link = document.createElement('a');
            link.href = `/api/v1/files/download/${encodeURIComponent(path)}`;
            link.download = path.split('/').pop();
            link.target = '_blank';
            
            // Add link to DOM temporarily
            document.body.appendChild(link);
            
            // Click the link
            link.click();
            
            // Remove link from DOM
            document.body.removeChild(link);
            
            this.showNotification('Descarga iniciada', 'success');
        } catch (error) {
            console.error('Download error:', error);
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
        pathParts.pop(); // Remove last directory
        this.currentPath = pathParts.join('/');
        this.loadExplorer();
    }

    async toggleDirectory(path) {
        const dirElement = document.querySelector(`[data-path="${path}"]`);
        const toggle = dirElement.querySelector('.directory-toggle');
        const content = dirElement.querySelector('.directory-content');
        
        if (content.classList.contains('expanded')) {
            // Collapse directory
            content.classList.remove('expanded');
            toggle.classList.remove('expanded');
        } else {
            // Expand directory
            try {
                // Load directory content
                const [subDirectories, files] = await Promise.all([
                    this.apiRequest('/directories'),
                    this.apiRequest(`/files/${encodeURIComponent(path)}`)
                ]);

                // Filter subdirectories for this directory
                const pathPrefix = path + '/';
                const relevantDirs = subDirectories.filter(dir => {
                    if (!dir.startsWith(pathPrefix)) return false;
                    const relativePath = dir.substring(pathPrefix.length);
                    return !relativePath.includes('/');
                });

                // Render directory content
                let contentHTML = '';
                
                if (relevantDirs.length === 0 && files.length === 0) {
                    contentHTML = '<div class="empty-state">Directorio vacío</div>';
                } else {
                    // Render subdirectories
                    relevantDirs.forEach(dir => {
                        const dirName = dir.split('/').pop();
                        contentHTML += `
                            <div class="explorer-item directory" data-path="${dir}">
                                <div class="directory-header">
                                    <div class="directory-toggle" onclick="event.stopPropagation(); pdfManager.toggleDirectory('${dir}')">
                                        <i class="fas fa-chevron-right"></i>
                                    </div>
                                    <div class="directory-icon">
                                        <i class="fas fa-folder"></i>
                                    </div>
                                    <span class="item-name" onclick="pdfManager.navigateTo('${dir}')">${dirName}</span>
                                    <div class="item-actions">
                                        <button class="action-icon delete" onclick="event.stopPropagation(); pdfManager.deleteDirectory('${dir}')" title="Eliminar">
                                            <i class="fas fa-trash"></i>
                                        </button>
                                    </div>
                                </div>
                                <div class="directory-content" id="content-${dir.replace(/[^a-zA-Z0-9]/g, '-')}">
                                    <div class="loading">Cargando...</div>
                                </div>
                            </div>
                        `;
                    });

                    // Render files
                    files.forEach(file => {
                        contentHTML += `
                            <div class="explorer-item file">
                                <div class="directory-header">
                                    <div class="directory-icon"></div>
                                    <div class="file-icon">
                                        <i class="fas fa-file-pdf"></i>
                                    </div>
                                    <span class="item-name">${file.name}</span>
                                    <div class="item-actions">
                                        <button class="action-icon" onclick="pdfManager.downloadFile('${file.path}')" title="Descargar">
                                            <i class="fas fa-download"></i>
                                        </button>
                                        <button class="action-icon delete" onclick="pdfManager.deleteFile('${file.path}')" title="Eliminar">
                                            <i class="fas fa-trash"></i>
                                        </button>
                                    </div>
                                </div>
                            </div>
                        `;
                    });
                }

                content.innerHTML = contentHTML;
                content.classList.add('expanded');
                toggle.classList.add('expanded');
                
            } catch (error) {
                console.error('Error loading directory content:', error);
                this.showNotification('Error al cargar contenido del directorio', 'error');
            }
        }
    }
}

// Global functions
window.closeModal = (modalId) => {
    document.getElementById(modalId).style.display = 'none';
};

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.pdfManager = new PDFManager();
}); 
window.listFiles = () => window.pdfManager.listFiles(); 