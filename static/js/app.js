/**
 * PDF Manager - Aplicación Principal
 * 
 * Coordina todos los módulos de la aplicación
 */

import { apiService } from './modules/api.js';
import { validationService } from './modules/validation.js';
import { uiService } from './modules/ui.js';
import { rendererService } from './modules/renderer.js';
import { fileManagerService } from './modules/fileManager.js';
import { documentManagerService } from './modules/documentManager.js';

class PDFManager {
    constructor() {
        this.currentPath = '';
        this.initializeEventListeners();
        this.loadExplorer();
    }

    /**
     * Inicializa todos los event listeners
     */
    initializeEventListeners() {
        // Botones principales
        document.getElementById('newFolderBtn')?.addEventListener('click', () => this.showFolderModal());
        document.getElementById('uploadBtn')?.addEventListener('click', () => this.showUploadModal());
        document.getElementById('refreshBtn')?.addEventListener('click', () => this.loadExplorer());

        // Formularios
        document.getElementById('createDirForm')?.addEventListener('submit', (e) => {
            e.preventDefault();
            this.createDirectory();
        });

        document.getElementById('uploadForm')?.addEventListener('submit', (e) => {
            e.preventDefault();
            this.uploadFile();
        });

        // Configurar drag and drop
        uiService.setupDragAndDrop();
    }

    /**
     * Muestra el modal de creación de directorio
     */
    showFolderModal() {
        // Obtener la ruta actual del fileManager
        const currentPath = fileManagerService.getCurrentPath();
        uiService.showFolderModal(currentPath);
    }

    /**
     * Muestra el modal de subida de archivos con metadatos
     */
    async showUploadModal() {
        // Sincronizar la ruta actual con el documentManager
        documentManagerService.setCurrentPath(fileManagerService.getCurrentPath());
        
        // Abrir modal de subida con metadatos
        await documentManagerService.openUploadModal();
    }

    /**
     * Cierra un modal
     */
    closeModal(modalId) {
        uiService.closeModal(modalId);
    }

    /**
     * Crea un directorio
     */
    async createDirectory() {
        await fileManagerService.createDirectory();
    }

    /**
     * Sube un archivo con metadatos
     */
    async uploadFile() {
        await documentManagerService.uploadDocumentWithMetadata();
    }

    /**
     * Carga el explorador
     */
    async loadExplorer() {
        await fileManagerService.loadExplorer();
    }

    /**
     * Renderiza el explorador
     */
    renderExplorer(directories, files) {
        rendererService.renderExplorer(directories, files, this.currentPath);
    }

    /**
     * Navega a una ruta específica
     */
    navigateTo(path) {
        fileManagerService.navigateTo(path);
        documentManagerService.setCurrentPath(path);
    }

    /**
     * Navega al directorio padre
     */
    navigateToParent() {
        fileManagerService.navigateToParent();
        documentManagerService.setCurrentPath(fileManagerService.getCurrentPath());
    }

    /**
     * Descarga un archivo
     */
    async downloadFile(path) {
        await fileManagerService.downloadFile(path);
    }

    /**
     * Elimina un archivo
     */
    async deleteFile(path) {
        await fileManagerService.deleteFile(path);
    }

    /**
     * Elimina un directorio
     */
    async deleteDirectory(path) {
        await fileManagerService.deleteDirectory(path);
    }

    /**
     * Alterna la expansión de un directorio
     */
    async toggleDirectory(path) {
        await fileManagerService.toggleDirectory(path);
    }

    /**
     * Muestra una notificación
     */
    showNotification(message, type = 'info') {
        uiService.showNotification(message, type);
    }

    /**
     * Confirma una acción
     */
    async confirm(message) {
        return uiService.confirm(message);
    }

    /**
     * Obtiene la ruta actual
     */
    getCurrentPath() {
        return fileManagerService.getCurrentPath();
    }

    /**
     * Establece la ruta actual
     */
    setCurrentPath(path) {
        fileManagerService.setCurrentPath(path);
        documentManagerService.setCurrentPath(path);
    }
}

// Inicializar la aplicación cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    // Crear instancia global
    window.pdfManager = new PDFManager();
    
    console.log('PDF Manager inicializado con módulos');
}); 