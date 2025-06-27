/**
 * API Module - Manejo de peticiones al backend
 */

export class ApiService {
    constructor(baseUrl = '/api/v1') {
        this.baseUrl = baseUrl;
    }

    async request(endpoint, options = {}) {
        try {
            const response = await fetch(`${this.baseUrl}${endpoint}`, {
                headers: {
                    'Accept': 'application/json',
                    ...options.headers
                },
                ...options
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                
                // Manejar errores de validación
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

            // Parsear respuesta según el tipo de contenido
            const contentType = response.headers.get('content-type');
            
            if (contentType && contentType.includes('application/json')) {
                return await response.json();
            } else {
                return await response.text();
            }
        } catch (error) {
            console.error('Error en petición API:', error);
            throw error;
        }
    }

    // Métodos para directorios
    async getDirectories() {
        return this.request('/directories');
    }

    async createDirectory(path) {
        const formData = new FormData();
        formData.append('path', path);
        
        return this.request('/directories', {
            method: 'POST',
            body: formData
        });
    }

    async deleteDirectory(path) {
        return this.request(`/directories/${encodeURIComponent(path)}`, {
            method: 'DELETE'
        });
    }

    // Métodos para archivos
    async getFiles(path) {
        return this.request(`/files/${encodeURIComponent(path)}`);
    }

    async uploadFile(file, path = '') {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('path', path);
        
        return this.request('/files/upload', {
            method: 'POST',
            body: formData
        });
    }

    async deleteFile(path) {
        return this.request(`/files/${encodeURIComponent(path)}`, {
            method: 'DELETE'
        });
    }

    getDownloadUrl(path) {
        return `${this.baseUrl}/files/download/${encodeURIComponent(path)}`;
    }

    // Método de salud
    async healthCheck() {
        return this.request('/health');
    }

    // ============================================================================
    // MÉTODOS PARA DOCUMENTOS CON METADATOS
    // ============================================================================

    /**
     * Sube un documento con metadatos
     */
    async uploadDocumentWithMetadata(file, path, documentTypeId, categoryId, clientId = null, uploadDate = null) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('path', path);
        formData.append('document_type_id', documentTypeId);
        formData.append('category_id', categoryId);
        
        if (clientId) {
            formData.append('client_id', clientId);
        }
        
        if (uploadDate) {
            formData.append('upload_date', uploadDate);
        }
        
        return this.request('/documents/upload', {
            method: 'POST',
            body: formData
        });
    }

    /**
     * Obtiene todos los tipos de documento
     */
    async getDocumentTypes() {
        return this.request('/documents/types');
    }

    /**
     * Obtiene todos los clientes
     */
    async getClients() {
        return this.request('/documents/clients');
    }

    /**
     * Obtiene todas las categorías
     */
    async getCategories() {
        return this.request('/documents/categories');
    }
}

// Instancia global del servicio API
export const apiService = new ApiService(); 