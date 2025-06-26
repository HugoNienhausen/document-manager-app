/**
 * UI Module - Manejo de elementos de interfaz de usuario
 */

export class UIService {
    constructor() {
        this.notifications = document.getElementById('notifications');
    }

    /**
     * Muestra una notificación
     */
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;

        this.notifications.appendChild(notification);

        // Auto-remover después de 3 segundos
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }

    /**
     * Muestra un modal
     */
    showModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.style.display = 'block';
        }
    }

    /**
     * Cierra un modal
     */
    closeModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.style.display = 'none';
            
            // Limpiar formularios
            const form = modal.querySelector('form');
            if (form) {
                form.reset();
            }
            
            // Limpiar zona de archivos
            const dropZone = modal.querySelector('.file-drop-zone');
            if (dropZone) {
                this.resetFileDropZone(dropZone);
            }
        }
    }

    /**
     * Muestra el modal de creación de directorio
     */
    showFolderModal(currentPath = '') {
        this.showModal('folderModal');
        
        // Actualizar información del modal
        const modalInfo = document.getElementById('modalInfo');
        if (modalInfo) {
            const location = currentPath ? `en "${currentPath}"` : 'en la raíz';
            modalInfo.innerHTML = `
                <p><i class="fas fa-info-circle"></i> El directorio se creará <span>${location}</span></p>
            `;
        }
    }

    /**
     * Muestra el modal de subida de archivos
     */
    showUploadModal() {
        this.showModal('uploadModal');
    }

    /**
     * Actualiza la etiqueta del archivo seleccionado
     */
    updateFileLabel(filename) {
        const dropZone = document.getElementById('fileDropZone');
        if (!dropZone) return;
        
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
    }

    /**
     * Resetea la zona de archivos
     */
    resetFileDropZone(dropZone) {
        const icon = dropZone.querySelector('i');
        const text = dropZone.querySelector('p');
        
        if (icon) {
            icon.className = 'fas fa-cloud-upload-alt';
        }
        
        if (text) {
            text.textContent = 'Arrastra un archivo PDF aquí o haz clic para seleccionar';
        }
    }

    /**
     * Configura drag and drop para archivos
     */
    setupDragAndDrop() {
        const dropZone = document.getElementById('fileDropZone');
        const fileInput = document.getElementById('pdfFile');

        if (!dropZone || !fileInput) return;

        // Click en la zona abre el selector de archivos
        dropZone.addEventListener('click', (e) => {
            // Evitar activar el input si se hace clic en elementos del modal
            if (e.target.closest('.modal-actions') || e.target.closest('button')) {
                return;
            }
            
            if (e.target !== fileInput) {
                fileInput.click();
            }
        });

        // Drag over
        dropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropZone.classList.add('dragover');
        });

        // Drag leave
        dropZone.addEventListener('dragleave', () => {
            dropZone.classList.remove('dragover');
        });

        // Drop
        dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropZone.classList.remove('dragover');
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                fileInput.files = files;
                this.updateFileLabel(files[0].name);
            }
        });

        // Cambio de archivo
        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                this.updateFileLabel(e.target.files[0].name);
            }
        });

        // Prevenir propagación del click en el input
        fileInput.addEventListener('click', (e) => {
            e.stopPropagation();
        });

        // Prevenir que los botones activen el input
        const modalActions = document.querySelector('.modal-actions');
        if (modalActions) {
            modalActions.addEventListener('click', (e) => {
                e.stopPropagation();
            });
        }
    }

    /**
     * Muestra un diálogo de confirmación
     */
    async confirm(message) {
        return new Promise((resolve) => {
            const overlay = document.createElement('div');
            overlay.className = 'confirm-overlay';
            overlay.innerHTML = `
                <div class="confirm-dialog">
                    <p>${message}</p>
                    <div class="confirm-actions">
                        <button class="btn btn-secondary" id="confirm-cancel">Cancelar</button>
                        <button class="btn btn-danger" id="confirm-ok">Confirmar</button>
                    </div>
                </div>
            `;

            document.body.appendChild(overlay);

            const handleConfirm = () => {
                cleanup();
                resolve(true);
            };

            const handleCancel = () => {
                cleanup();
                resolve(false);
            };

            const cleanup = () => {
                document.body.removeChild(overlay);
            };

            overlay.querySelector('#confirm-ok').addEventListener('click', handleConfirm);
            overlay.querySelector('#confirm-cancel').addEventListener('click', handleCancel);
            overlay.addEventListener('click', (e) => {
                if (e.target === overlay) handleCancel();
            });
        });
    }

    /**
     * Muestra un indicador de carga
     */
    showLoading(elementId, message = 'Cargando...') {
        const element = document.getElementById(elementId);
        if (element) {
            element.innerHTML = `<div class="loading">${message}</div>`;
        }
    }

    /**
     * Oculta el indicador de carga
     */
    hideLoading(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            const loading = element.querySelector('.loading');
            if (loading) {
                loading.remove();
            }
        }
    }

    /**
     * Actualiza el breadcrumb
     */
    updateBreadcrumb(currentPath) {
        const breadcrumb = document.getElementById('breadcrumb');
        const currentPathElement = document.getElementById('currentPath');
        
        if (!breadcrumb) return;

        const pathParts = currentPath ? currentPath.split('/').filter(part => part) : [];
        
        let breadcrumbHTML = `
            <div class="breadcrumb-item ${pathParts.length === 0 ? 'active' : ''}" 
                 onclick="pdfManager.navigateTo('')" title="Ir al inicio">
                <i class="fas fa-home"></i>
                <span>Inicio</span>
            </div>
        `;

        let currentFullPath = '';
        pathParts.forEach((part, index) => {
            currentFullPath += (currentFullPath ? '/' : '') + part;
            const isLast = index === pathParts.length - 1;
            
            breadcrumbHTML += `
                <div class="breadcrumb-separator">
                    <i class="fas fa-chevron-right"></i>
                </div>
                <div class="breadcrumb-item ${isLast ? 'active' : ''}" 
                     onclick="pdfManager.navigateTo('${currentFullPath}')" 
                     title="${isLast ? 'Ubicación actual' : `Ir a ${part}`}">
                    <i class="fas fa-folder"></i>
                    <span>${part}</span>
                </div>
            `;
        });

        breadcrumb.innerHTML = breadcrumbHTML;
        
        // Actualizar indicador de ruta en el header
        if (currentPathElement) {
            const pathSpan = currentPathElement.querySelector('span');
            if (pathSpan) {
                if (pathParts.length === 0) {
                    pathSpan.textContent = 'Inicio';
                } else {
                    pathSpan.textContent = pathParts[pathParts.length - 1];
                }
            }
        }
        
        // Actualizar título de la página
        const pageTitle = pathParts.length > 0 ? `${pathParts[pathParts.length - 1]} - PDF Manager` : 'PDF Manager';
        document.title = pageTitle;
    }
}

// Instancia global del servicio UI
export const uiService = new UIService(); 