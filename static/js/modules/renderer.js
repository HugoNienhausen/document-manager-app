/**
 * Renderer Module - Renderizado de elementos de la interfaz
 */

export class RendererService {
    constructor() {
        this.explorerList = document.getElementById('explorerList');
    }

    /**
     * Renderiza el explorador principal
     */
    renderExplorer(directories, files, currentPath = '') {
        if (!this.explorerList) return;

        let explorerHTML = '';

        // Renderizar directorio padre si estamos en un subdirectorio
        if (currentPath) {
            explorerHTML += `
                <div class="explorer-item directory parent-dir" onclick="pdfManager.navigateToParent()">
                    <div class="directory-header">
                        <div class="directory-icon">
                            <i class="fas fa-arrow-up"></i>
                        </div>
                        <span class="item-name">..</span>
                    </div>
                </div>
            `;
        }

        // Renderizar directorios
        if (directories.length > 0) {
            directories.forEach(directory => {
                // Construir la ruta completa para el directorio
                const fullPath = currentPath ? `${currentPath}/${directory}` : directory;
                
                explorerHTML += `
                    <div class="explorer-item directory">
                        <div class="directory-header">
                            <div class="directory-toggle" onclick="pdfManager.toggleDirectory('${fullPath}')">
                                <i class="fas fa-chevron-right"></i>
                            </div>
                            <div class="directory-icon">
                                <i class="fas fa-folder"></i>
                            </div>
                            <span class="item-name" onclick="pdfManager.navigateTo('${fullPath}')">${directory}</span>
                            <div class="item-actions">
                                <button class="action-icon delete" onclick="event.stopPropagation(); pdfManager.deleteDirectory('${fullPath}')" title="Eliminar">
                                    <i class="fas fa-trash"></i>
                                </button>
                            </div>
                        </div>
                        <div class="directory-content" id="content-${fullPath.replace(/\//g, '-')}"></div>
                    </div>
                `;
            });
        }

        // Renderizar archivos en el directorio actual
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
        } else if (!currentPath && directories.length === 0) {
            explorerHTML += '<div class="empty-state">No hay archivos PDF</div>';
        }

        this.explorerList.innerHTML = explorerHTML;
    }

    /**
     * Renderiza el contenido de un directorio expandido
     */
    renderDirectoryContent(directoryPath, subdirectories = [], files = []) {
        const contentElement = document.getElementById(`content-${directoryPath.replace(/\//g, '-')}`);
        if (!contentElement) return;

        let contentHTML = '';

        // Renderizar subdirectorios
        if (subdirectories.length > 0) {
            subdirectories.forEach(subdirectory => {
                // Construir la ruta completa para el subdirectorio
                const fullSubPath = `${directoryPath}/${subdirectory}`;
                
                contentHTML += `
                    <div class="explorer-item directory">
                        <div class="directory-header">
                            <div class="directory-toggle" onclick="pdfManager.toggleDirectory('${fullSubPath}')">
                                <i class="fas fa-chevron-right"></i>
                            </div>
                            <div class="directory-icon">
                                <i class="fas fa-folder"></i>
                            </div>
                            <span class="item-name" onclick="pdfManager.navigateTo('${fullSubPath}')">${subdirectory}</span>
                            <div class="item-actions">
                                <button class="action-icon delete" onclick="event.stopPropagation(); pdfManager.deleteDirectory('${fullSubPath}')" title="Eliminar">
                                    <i class="fas fa-trash"></i>
                                </button>
                            </div>
                        </div>
                        <div class="directory-content" id="content-${fullSubPath.replace(/\//g, '-')}"></div>
                    </div>
                `;
            });
        }

        // Renderizar archivos
        if (files.length > 0) {
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

        // Mostrar mensaje si no hay contenido
        if (subdirectories.length === 0 && files.length === 0) {
            contentHTML += '<div class="empty-state">No hay contenido en este directorio</div>';
        }

        contentElement.innerHTML = contentHTML;
    }

    /**
     * Expande un directorio en la vista
     */
    expandDirectory(directoryPath) {
        const toggle = document.querySelector(`[onclick="pdfManager.toggleDirectory('${directoryPath}')"]`);
        const contentElement = document.getElementById(`content-${directoryPath.replace(/\//g, '-')}`);

        if (toggle) {
            toggle.classList.add('expanded');
        }

        if (contentElement) {
            contentElement.classList.add('expanded');
        }
    }

    /**
     * Colapsa un directorio en la vista
     */
    collapseDirectory(directoryPath) {
        const toggle = document.querySelector(`[onclick="pdfManager.toggleDirectory('${directoryPath}')"]`);
        const contentElement = document.getElementById(`content-${directoryPath.replace(/\//g, '-')}`);

        if (toggle) {
            toggle.classList.remove('expanded');
        }

        if (contentElement) {
            contentElement.classList.remove('expanded');
        }
    }

    /**
     * Renderiza una lista simple de directorios
     */
    renderDirectoryList(directories) {
        if (!this.explorerList) return;

        let html = '';
        
        if (directories.length > 0) {
            directories.forEach(directory => {
                html += `
                    <div class="list-item directory" onclick="pdfManager.navigateTo('${directory}')">
                        <i class="fas fa-folder"></i>
                        <span class="name">${directory}</span>
                    </div>
                `;
            });
        } else {
            html = '<div class="empty-state">No hay directorios</div>';
        }

        this.explorerList.innerHTML = html;
    }

    /**
     * Renderiza una lista simple de archivos
     */
    renderFileList(files) {
        if (!this.explorerList) return;

        let html = '';
        
        if (files.length > 0) {
            files.forEach(file => {
                html += `
                    <div class="list-item file">
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
                `;
            });
        } else {
            html = '<div class="empty-state">No hay archivos</div>';
        }

        this.explorerList.innerHTML = html;
    }

    /**
     * Actualiza el estado de carga
     */
    showLoadingState(message = 'Cargando...') {
        if (this.explorerList) {
            this.explorerList.innerHTML = `<div class="loading">${message}</div>`;
        }
    }

    /**
     * Muestra estado vacío
     */
    showEmptyState(message = 'No hay elementos para mostrar') {
        if (this.explorerList) {
            this.explorerList.innerHTML = `<div class="empty-state">${message}</div>`;
        }
    }

    /**
     * Actualiza el contador de archivos
     */
    updateFileCount(count) {
        const countElement = document.getElementById('fileCount');
        if (countElement) {
            countElement.textContent = `${count} archivo${count !== 1 ? 's' : ''}`;
        }
    }

    /**
     * Actualiza el título del explorador
     */
    updateExplorerTitle(title) {
        const titleElement = document.querySelector('.explorer-header h2');
        if (titleElement) {
            titleElement.textContent = title;
        }
    }
}

// Instancia global del servicio de renderizado
export const rendererService = new RendererService(); 