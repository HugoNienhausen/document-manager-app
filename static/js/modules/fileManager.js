/**
 * File Manager Module - Gestión de archivos
 */

import { apiService } from './api.js';
import { validationService } from './validation.js';
import { uiService } from './ui.js';
import { rendererService } from './renderer.js';

export class FileManagerService {
    constructor() {
        this.currentPath = '';
    }

    /**
     * Sube un archivo PDF
     */
    async uploadFile() {
        const fileInput = document.getElementById('pdfFile');
        
        if (!fileInput) {
            uiService.showNotification('Error: No se pudo acceder al selector de archivos', 'error');
            return;
        }
        
        const file = fileInput.files[0];

        // Validar archivo
        const validation = validationService.validatePdfFile(file);
        if (!validation.isValid) {
            uiService.showNotification(validation.errors[0], 'error');
            return;
        }

        try {
            const result = await apiService.uploadFile(file, this.currentPath || '');
            
            uiService.showNotification('Archivo subido exitosamente', 'success');
            uiService.closeModal('uploadModal');
            
            // Recargar explorador
            this.loadExplorer();
        } catch (error) {
            console.error('Error al subir archivo:', error);
            uiService.showNotification(error.message, 'error');
        }
    }

    /**
     * Descarga un archivo
     */
    async downloadFile(path) {
        try {
            // Crear enlace temporal de descarga
            const link = document.createElement('a');
            link.href = apiService.getDownloadUrl(path);
            link.download = path.split('/').pop();
            link.target = '_blank';
            
            // Agregar enlace al DOM temporalmente
            document.body.appendChild(link);
            
            // Hacer clic en el enlace
            link.click();
            
            // Remover enlace del DOM
            document.body.removeChild(link);
            
            uiService.showNotification('Descarga iniciada', 'success');
        } catch (error) {
            console.error('Error al descargar:', error);
            uiService.showNotification(`Error al descargar: ${error.message}`, 'error');
        }
    }

    /**
     * Elimina un archivo
     */
    async deleteFile(path) {
        const confirmed = await uiService.confirm('¿Eliminar este archivo?');
        if (!confirmed) return;

        try {
            await apiService.deleteFile(path);
            uiService.showNotification('Archivo eliminado', 'success');
            this.loadExplorer();
        } catch (error) {
            uiService.showNotification(error.message, 'error');
        }
    }

    /**
     * Elimina un directorio
     */
    async deleteDirectory(path) {
        const confirmed = await uiService.confirm('¿Eliminar este directorio y todo su contenido?');
        if (!confirmed) return;

        try {
            await apiService.deleteDirectory(path);
            uiService.showNotification('Directorio eliminado', 'success');
            this.loadExplorer();
        } catch (error) {
            uiService.showNotification(error.message, 'error');
        }
    }

    /**
     * Crea un directorio
     */
    async createDirectory() {
        const nameInput = document.getElementById('dirName');
        const directoryName = nameInput.value.trim();

        // Validar nombre del directorio
        const validation = validationService.validateDirectoryName(directoryName);
        if (!validation.isValid) {
            uiService.showNotification(validation.errors[0], 'error');
            return;
        }

        try {
            // Construir ruta completa
            const fullPath = this.currentPath ? `${this.currentPath}/${directoryName}` : directoryName;
            
            await apiService.createDirectory(fullPath);
            
            uiService.showNotification('Directorio creado exitosamente', 'success');
            uiService.closeModal('folderModal');
            this.loadExplorer();
        } catch (error) {
            uiService.showNotification(error.message, 'error');
        }
    }

    /**
     * Carga el explorador con directorios y archivos
     */
    async loadExplorer() {
        try {
            rendererService.showLoadingState('Cargando explorador...');
            
            // Cargar directorios
            const directories = await apiService.getDirectories();
            
            // Filtrar directorios para la ruta actual
            const filteredDirectories = this.filterDirectoriesForCurrentPath(directories);
            
            // Cargar archivos del directorio actual
            let files = [];
            if (this.currentPath) {
                try {
                    files = await apiService.getFiles(this.currentPath);
                } catch (error) {
                    console.warn('No se pudieron cargar archivos:', error);
                }
            }
            
            // Renderizar explorador
            rendererService.renderExplorer(filteredDirectories, files, this.currentPath);
            
            // Actualizar breadcrumb
            uiService.updateBreadcrumb(this.currentPath);
            
        } catch (error) {
            console.error('Error al cargar explorador:', error);
            uiService.showNotification('Error al cargar el explorador', 'error');
            rendererService.showEmptyState('Error al cargar contenido');
        }
    }

    /**
     * Filtra directorios para la ruta actual
     */
    filterDirectoriesForCurrentPath(allDirectories) {
        if (!this.currentPath) {
            // En la raíz, mostrar solo directorios de primer nivel
            return allDirectories.filter(dir => !dir.includes('/'));
        } else {
            // En un subdirectorio, mostrar solo directorios directos
            const prefix = `${this.currentPath}/`;
            return allDirectories.filter(dir => 
                dir.startsWith(prefix) && 
                dir.substring(prefix.length).indexOf('/') === -1
            ).map(dir => dir.substring(prefix.length));
        }
    }

    /**
     * Navega a una ruta específica
     */
    navigateTo(path) {
        this.currentPath = path;
        this.loadExplorer();
    }

    /**
     * Navega al directorio padre
     */
    navigateToParent() {
        if (this.currentPath) {
            const pathParts = this.currentPath.split('/');
            pathParts.pop();
            this.currentPath = pathParts.join('/');
            this.loadExplorer();
        }
    }

    /**
     * Alterna la expansión de un directorio
     */
    async toggleDirectory(path) {
        const toggle = document.querySelector(`[onclick="pdfManager.toggleDirectory('${path}')"]`);
        const content = document.getElementById(`content-${path.replace(/\//g, '-')}`);
        
        if (!toggle || !content) return;

        if (toggle.classList.contains('expanded')) {
            // Colapsar
            toggle.classList.remove('expanded');
            content.classList.remove('expanded');
        } else {
            // Expandir
            toggle.classList.add('expanded');
            content.classList.add('expanded');
            
            try {
                // Cargar todos los directorios
                const allDirectories = await apiService.getDirectories();
                
                // Filtrar subdirectorios del directorio actual
                const subdirectories = this.filterDirectoriesForPath(allDirectories, path);
                
                // Cargar archivos del directorio
                const files = await apiService.getFiles(path);
                
                // Renderizar contenido (subdirectorios y archivos)
                rendererService.renderDirectoryContent(path, subdirectories, files);
                
            } catch (error) {
                console.error('Error al cargar contenido del directorio:', error);
                uiService.showNotification('Error al cargar contenido del directorio', 'error');
            }
        }
    }

    /**
     * Filtra directorios para una ruta específica (para expansión)
     */
    filterDirectoriesForPath(allDirectories, path) {
        const prefix = path ? `${path}/` : '';
        return allDirectories.filter(dir => 
            dir.startsWith(prefix) && 
            dir.substring(prefix.length).indexOf('/') === -1
        ).map(dir => dir.substring(prefix.length));
    }

    /**
     * Obtiene la ruta actual
     */
    getCurrentPath() {
        return this.currentPath;
    }

    /**
     * Establece la ruta actual
     */
    setCurrentPath(path) {
        this.currentPath = path;
    }
}

// Instancia global del servicio de gestión de archivos
export const fileManagerService = new FileManagerService(); 