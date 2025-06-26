/**
 * Validation Module - Validación de archivos y formularios
 */

export class ValidationService {
    constructor() {
        this.maxFileSize = 50 * 1024 * 1024; // 50MB
        this.allowedExtensions = ['.pdf'];
    }

    /**
     * Valida un archivo PDF
     */
    validatePdfFile(file) {
        const errors = [];

        // Verificar que se seleccionó un archivo
        if (!file) {
            errors.push('Por favor selecciona un archivo PDF');
            return { isValid: false, errors };
        }

        // Verificar extensión
        const fileName = file.name.toLowerCase();
        const hasValidExtension = this.allowedExtensions.some(ext => 
            fileName.endsWith(ext)
        );

        if (!hasValidExtension) {
            errors.push('Por favor selecciona solo archivos PDF');
        }

        // Verificar tamaño
        if (file.size > this.maxFileSize) {
            const maxSizeMB = this.maxFileSize / (1024 * 1024);
            errors.push(`El archivo es demasiado grande. Máximo ${maxSizeMB}MB`);
        }

        return {
            isValid: errors.length === 0,
            errors
        };
    }

    /**
     * Valida el nombre de un directorio
     */
    validateDirectoryName(name) {
        const errors = [];

        if (!name || name.trim().length === 0) {
            errors.push('El nombre del directorio no puede estar vacío');
        }

        if (name && name.length > 255) {
            errors.push('El nombre del directorio es demasiado largo (máximo 255 caracteres)');
        }

        // Caracteres no permitidos en nombres de directorio
        const invalidChars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|'];
        const hasInvalidChars = invalidChars.some(char => name.includes(char));
        
        if (hasInvalidChars) {
            errors.push('El nombre del directorio contiene caracteres no permitidos');
        }

        return {
            isValid: errors.length === 0,
            errors
        };
    }

    /**
     * Valida una ruta de directorio
     */
    validateDirectoryPath(path) {
        const errors = [];

        if (path && path.length > 500) {
            errors.push('La ruta del directorio es demasiado larga');
        }

        // Verificar que no contenga rutas relativas peligrosas
        if (path && (path.includes('..') || path.includes('./'))) {
            errors.push('La ruta del directorio no puede contener rutas relativas');
        }

        return {
            isValid: errors.length === 0,
            errors
        };
    }

    /**
     * Sanitiza un nombre de archivo
     */
    sanitizeFilename(filename) {
        if (!filename) return '';
        
        // Eliminar caracteres peligrosos
        const dangerousChars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|'];
        let sanitized = filename;
        
        dangerousChars.forEach(char => {
            sanitized = sanitized.replace(char, '_');
        });

        return sanitized;
    }

    /**
     * Formatea el tamaño de archivo para mostrar
     */
    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';

        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));

        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    /**
     * Valida un formulario completo
     */
    validateForm(formData) {
        const errors = {};

        // Validar campos requeridos
        Object.keys(formData).forEach(field => {
            const value = formData[field];
            
            if (value === undefined || value === null || value === '') {
                errors[field] = `El campo ${field} es requerido`;
            }
        });

        return {
            isValid: Object.keys(errors).length === 0,
            errors
        };
    }
}

// Instancia global del servicio de validación
export const validationService = new ValidationService(); 