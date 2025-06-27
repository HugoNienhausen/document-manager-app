/**
 * Document Manager Module - Gestión de documentos con metadatos
 */

import { apiService } from './api.js';
import { validationService } from './validation.js';
import { uiService } from './ui.js';
import { rendererService } from './renderer.js';

export class DocumentManagerService {
    constructor() {
        this.currentPath = '';
        this.documentTypes = [];
        this.clients = [];
        this.categories = [];
        this.isInitialized = false;
    }

    /**
     * Inicializa el servicio cargando los metadatos necesarios
     */
    async initialize() {
        if (this.isInitialized) return;

        try {
            // Cargar tipos de documento, clientes y categorías
            const [types, clients, categories] = await Promise.all([
                apiService.getDocumentTypes(),
                apiService.getClients(),
                apiService.getCategories()
            ]);

            this.documentTypes = types;
            this.clients = clients;
            this.categories = categories;
            this.isInitialized = true;

            console.log('DocumentManager inicializado:', {
                types: this.documentTypes.length,
                clients: this.clients.length,
                categories: this.categories.length
            });
        } catch (error) {
            console.error('Error al inicializar DocumentManager:', error);
            uiService.showNotification('Error al cargar metadatos de documentos', 'error');
        }
    }

    /**
     * Abre el modal de subida de documento con metadatos
     */
    async openUploadModal() {
        await this.initialize();
        this.showUploadModal();
    }

    /**
     * Muestra el modal de subida con campos de metadatos
     */
    showUploadModal() {
        const modal = document.getElementById('uploadModal');
        if (!modal) {
            uiService.showNotification('Error: Modal de subida no encontrado', 'error');
            return;
        }

        // Limpiar formulario anterior
        this.clearUploadForm();

        // Llenar selectores con datos
        this.populateDocumentTypeSelect();
        this.populateClientSelect();
        this.populateCategorySelect();

        // Mostrar modal
        uiService.showModal('uploadModal');
    }

    /**
     * Limpia el formulario de subida
     */
    clearUploadForm() {
        const fileInput = document.getElementById('pdfFile');
        const documentTypeSelect = document.getElementById('documentType');
        const clientSelect = document.getElementById('client');
        const categorySelect = document.getElementById('category');
        const uploadDateInput = document.getElementById('uploadDate');

        if (fileInput) fileInput.value = '';
        if (documentTypeSelect) documentTypeSelect.value = '';
        if (clientSelect) clientSelect.value = '';
        if (categorySelect) categorySelect.value = '';
        if (uploadDateInput) uploadDateInput.value = '';
    }

    /**
     * Llena el selector de tipos de documento
     */
    populateDocumentTypeSelect() {
        const select = document.getElementById('documentType');
        if (!select) return;

        select.innerHTML = '<option value="">Seleccionar tipo de documento</option>';
        
        this.documentTypes.forEach(type => {
            const option = document.createElement('option');
            option.value = type.id;
            option.textContent = type.name;
            if (type.description) {
                option.title = type.description;
            }
            select.appendChild(option);
        });
    }

    /**
     * Llena el selector de clientes
     */
    populateClientSelect() {
        const select = document.getElementById('client');
        if (!select) return;

        select.innerHTML = '<option value="">Sin cliente (opcional)</option>';
        
        this.clients.forEach(client => {
            const option = document.createElement('option');
            option.value = client.id;
            option.textContent = client.name;
            if (client.email) {
                option.title = `${client.email}${client.phone ? ` - ${client.phone}` : ''}`;
            }
            select.appendChild(option);
        });
    }

    /**
     * Llena el selector de categorías
     */
    populateCategorySelect() {
        const select = document.getElementById('category');
        if (!select) return;

        select.innerHTML = '<option value="">Seleccionar categoría</option>';
        
        this.categories.forEach(category => {
            const option = document.createElement('option');
            option.value = category.id;
            option.textContent = category.name;
            if (category.description) {
                option.title = category.description;
            }
            select.appendChild(option);
        });
    }

    /**
     * Sube un documento con metadatos
     */
    async uploadDocumentWithMetadata() {
        const fileInput = document.getElementById('pdfFile');
        const documentTypeSelect = document.getElementById('documentType');
        const clientSelect = document.getElementById('client');
        const categorySelect = document.getElementById('category');
        const uploadDateInput = document.getElementById('uploadDate');

        if (!fileInput || !documentTypeSelect || !categorySelect) {
            uiService.showNotification('Error: Formulario incompleto', 'error');
            return;
        }

        const file = fileInput.files[0];
        const documentTypeId = parseInt(documentTypeSelect.value);
        const clientId = clientSelect.value ? parseInt(clientSelect.value) : null;
        const categoryId = parseInt(categorySelect.value);
        const uploadDate = uploadDateInput.value;

        // Validar archivo
        const fileValidation = validationService.validatePdfFile(file);
        if (!fileValidation.isValid) {
            uiService.showNotification(fileValidation.errors[0], 'error');
            return;
        }

        // Validar metadatos
        const metadataValidation = this.validateMetadata(documentTypeId, categoryId);
        if (!metadataValidation.isValid) {
            uiService.showNotification(metadataValidation.errors[0], 'error');
            return;
        }

        try {
            uiService.showLoading('explorerList', 'Subiendo documento...');

            const result = await apiService.uploadDocumentWithMetadata(
                file,
                this.currentPath || '',
                documentTypeId,
                categoryId,
                clientId,
                uploadDate
            );

            uiService.hideLoading('explorerList');
            uiService.showNotification('Documento subido y registrado exitosamente', 'success');
            uiService.closeModal('uploadModal');

            // Mostrar información del documento creado
            this.showDocumentInfo(result.document);

            // Recargar explorador
            this.loadExplorer();
        } catch (error) {
            uiService.hideLoading('explorerList');
            console.error('Error al subir documento:', error);
            uiService.showNotification(error.message, 'error');
        }
    }

    /**
     * Valida los metadatos del documento
     */
    validateMetadata(documentTypeId, categoryId) {
        const errors = [];

        if (!documentTypeId || documentTypeId <= 0) {
            errors.push('Debe seleccionar un tipo de documento');
        }

        if (!categoryId || categoryId <= 0) {
            errors.push('Debe seleccionar una categoría');
        }

        return {
            isValid: errors.length === 0,
            errors: errors
        };
    }

    /**
     * Muestra información del documento creado
     */
    showDocumentInfo(document) {
        const info = `
            <div class="document-info">
                <h4>Documento registrado exitosamente</h4>
                <p><strong>Archivo:</strong> ${document.filename}</p>
                <p><strong>Tipo:</strong> ${document.document_type}</p>
                <p><strong>Categoría:</strong> ${document.category}</p>
                ${document.client ? `<p><strong>Cliente:</strong> ${document.client}</p>` : ''}
                <p><strong>Tamaño:</strong> ${this.formatFileSize(document.file_size)}</p>
                <p><strong>Fecha de subida:</strong> ${new Date(document.upload_date).toLocaleString()}</p>
                <p><strong>Hash:</strong> <code>${document.file_hash.substring(0, 16)}...</code></p>
            </div>
        `;

        uiService.showNotification(info, 'success');
    }

    /**
     * Formatea el tamaño del archivo
     */
    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    /**
     * Carga el explorador (delegado al FileManager)
     */
    async loadExplorer() {
        // Este método se delega al FileManager desde la aplicación principal
        console.log('DocumentManager: loadExplorer llamado');
    }

    /**
     * Establece la ruta actual
     */
    setCurrentPath(path) {
        this.currentPath = path;
    }

    /**
     * Obtiene la ruta actual
     */
    getCurrentPath() {
        return this.currentPath;
    }
}

// Exportar instancia singleton
export const documentManagerService = new DocumentManagerService(); 