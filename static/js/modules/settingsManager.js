/**
 * Settings Manager Module
 * Maneja la configuración de metadatos (tipos de documento, categorías, clientes)
 */

import { apiService } from './api.js';
import { notificationService } from './notifications.js';
import { uiService } from './ui.js';

export class SettingsManagerService {
    constructor() {
        this.currentTab = 'document-types';
        this.editingItem = null;
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // Config button
        const configBtn = document.getElementById('configBtn');
        const configDropdown = document.getElementById('configDropdown');

        if (configBtn && configDropdown) {
            configBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                this.toggleConfigDropdown();
            });

            // Close dropdown when clicking outside
            document.addEventListener('click', (e) => {
                if (!configBtn.contains(e.target) && !configDropdown.contains(e.target)) {
                    this.hideConfigDropdown();
                }
            });

            // Config menu items
            configDropdown.addEventListener('click', (e) => {
                const configItem = e.target.closest('.config-item');
                if (configItem) {
                    const action = configItem.dataset.action;
                    this.handleConfigAction(action);
                }
            });
        }

        // Tab buttons
        document.addEventListener('click', (e) => {
            if (e.target.closest('.tab-btn')) {
                const tabBtn = e.target.closest('.tab-btn');
                const tabName = tabBtn.dataset.tab;
                this.switchTab(tabName);
            }
        });
    }

    toggleConfigDropdown() {
        const dropdown = document.getElementById('configDropdown');
        dropdown.classList.toggle('show');
    }

    hideConfigDropdown() {
        const dropdown = document.getElementById('configDropdown');
        dropdown.classList.remove('show');
    }

    handleConfigAction(action) {
        this.hideConfigDropdown();
        
        switch (action) {
            case 'metadata':
                this.openMetadataModal();
                break;
            case 'settings':
                notificationService.showInfo('Configuración general próximamente disponible');
                break;
            case 'about':
                notificationService.showInfo('Gestor de PDFs v1.0.0 - Desarrollado con FastAPI y JavaScript');
                break;
        }
    }

    openMetadataModal() {
        const modal = document.getElementById('metadataModal');
        if (modal) {
            modal.style.display = 'flex';
            this.loadMetadataSettings();
        }
    }

    closeMetadataModal() {
        const modal = document.getElementById('metadataModal');
        if (modal) {
            modal.style.display = 'none';
            this.resetForm();
        }
    }

    switchTab(tabName) {
        // Update tab buttons
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');

        // Update tab panes
        document.querySelectorAll('.tab-pane').forEach(pane => {
            pane.classList.remove('active');
        });
        document.getElementById(`${tabName}-tab`).classList.add('active');

        this.currentTab = tabName;
        this.loadTabContent(tabName);
    }

    async loadMetadataSettings() {
        try {
            await this.loadTabContent(this.currentTab);
        } catch (error) {
            console.error('Error loading metadata settings:', error);
            notificationService.showError('Error al cargar la configuración de metadatos');
        }
    }

    async loadTabContent(tabName) {
        switch (tabName) {
            case 'document-types':
                await this.loadDocumentTypes();
                break;
            case 'categories':
                await this.loadCategories();
                break;
            case 'clients':
                await this.loadClients();
                break;
        }
    }

    async loadDocumentTypes() {
        try {
            const documentTypes = await apiService.getDocumentTypes();
            this.renderDocumentTypes(documentTypes);
        } catch (error) {
            console.error('Error loading document types:', error);
            notificationService.showError('Error al cargar tipos de documento');
        }
    }

    async loadCategories() {
        try {
            const categories = await apiService.getCategories();
            this.renderCategories(categories);
        } catch (error) {
            console.error('Error loading categories:', error);
            notificationService.showError('Error al cargar categorías');
        }
    }

    async loadClients() {
        try {
            const clients = await apiService.getClients();
            this.renderClients(clients);
        } catch (error) {
            console.error('Error loading clients:', error);
            notificationService.showError('Error al cargar clientes');
        }
    }

    renderDocumentTypes(documentTypes) {
        const container = document.getElementById('documentTypesList');
        if (!container) return;

        container.innerHTML = documentTypes.length === 0 
            ? '<p class="empty-state">No hay tipos de documento configurados</p>'
            : documentTypes.map(type => this.createMetadataItem(type, 'document-type')).join('');
    }

    renderCategories(categories) {
        const container = document.getElementById('categoriesList');
        if (!container) return;

        container.innerHTML = categories.length === 0 
            ? '<p class="empty-state">No hay categorías configuradas</p>'
            : categories.map(category => this.createMetadataItem(category, 'category')).join('');
    }

    renderClients(clients) {
        const container = document.getElementById('clientsList');
        if (!container) return;

        container.innerHTML = clients.length === 0 
            ? '<p class="empty-state">No hay clientes configurados</p>'
            : clients.map(client => this.createMetadataItem(client, 'client')).join('');
    }

    createMetadataItem(item, type) {
        const description = item.description || 'Sin descripción';
        const email = item.email ? ` • ${item.email}` : '';
        const phone = item.phone ? ` • ${item.phone}` : '';
        
        return `
            <div class="metadata-item" data-id="${item.id}" data-type="${type}">
                <div class="metadata-info">
                    <div class="metadata-name">${item.name}</div>
                    <div class="metadata-description">${description}${email}${phone}</div>
                </div>
                <div class="metadata-actions">
                    <button class="edit-btn" onclick="settingsManager.editItem(${item.id}, '${type}')">
                        <i class="fas fa-edit"></i> Editar
                    </button>
                    <button class="delete-btn" onclick="settingsManager.deleteItem(${item.id}, '${type}')">
                        <i class="fas fa-trash"></i> Eliminar
                    </button>
                </div>
            </div>
        `;
    }

    addDocumentType() {
        this.showAddForm('document-type', {
            name: '',
            description: ''
        });
    }

    addCategory() {
        this.showAddForm('category', {
            name: '',
            description: ''
        });
    }

    addClient() {
        this.showAddForm('client', {
            name: '',
            email: '',
            phone: ''
        });
    }

    showAddForm(type, data = {}) {
        const container = this.getCurrentListContainer();
        if (!container) return;

        const formHtml = this.createFormHtml(type, data);
        container.insertAdjacentHTML('beforeend', formHtml);
        
        // Scroll to the new form
        const newForm = container.querySelector('.metadata-form');
        if (newForm) {
            newForm.scrollIntoView({ behavior: 'smooth' });
        }
    }

    editItem(id, type) {
        const item = document.querySelector(`[data-id="${id}"][data-type="${type}"]`);
        if (!item) return;

        const name = item.querySelector('.metadata-name').textContent;
        const description = item.querySelector('.metadata-description').textContent;
        
        let data = { id, name, description };
        
        if (type === 'client') {
            const parts = description.split(' • ');
            data.email = parts[1] || '';
            data.phone = parts[2] || '';
        }

        this.showEditForm(type, data);
    }

    showEditForm(type, data) {
        const container = this.getCurrentListContainer();
        if (!container) return;

        const formHtml = this.createFormHtml(type, data, true);
        container.insertAdjacentHTML('beforeend', formHtml);
        
        // Scroll to the new form
        const newForm = container.querySelector('.metadata-form');
        if (newForm) {
            newForm.scrollIntoView({ behavior: 'smooth' });
        }
    }

    createFormHtml(type, data, isEdit = false) {
        const action = isEdit ? 'Actualizar' : 'Crear';
        const icon = isEdit ? 'fa-save' : 'fa-plus';
        
        let fields = '';
        
        if (type === 'client') {
            fields = `
                <div class="form-row">
                    <div class="form-group">
                        <label for="name">Nombre *</label>
                        <input type="text" id="name" value="${data.name || ''}" required>
                    </div>
                    <div class="form-group">
                        <label for="email">Email</label>
                        <input type="email" id="email" value="${data.email || ''}">
                    </div>
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label for="phone">Teléfono</label>
                        <input type="tel" id="phone" value="${data.phone || ''}">
                    </div>
                </div>
            `;
        } else {
            fields = `
                <div class="form-row">
                    <div class="form-group">
                        <label for="name">Nombre *</label>
                        <input type="text" id="name" value="${data.name || ''}" required>
                    </div>
                    <div class="form-group">
                        <label for="description">Descripción</label>
                        <textarea id="description">${data.description || ''}</textarea>
                    </div>
                </div>
            `;
        }

        return `
            <div class="metadata-form" data-type="${type}" data-id="${data.id || ''}">
                <h5>
                    <i class="fas ${icon}"></i>
                    ${isEdit ? 'Editar' : 'Agregar'} ${this.getTypeLabel(type)}
                </h5>
                ${fields}
                <div class="form-actions">
                    <button type="button" class="btn btn-secondary" onclick="settingsManager.cancelForm()">
                        Cancelar
                    </button>
                    <button type="button" class="btn btn-primary" onclick="settingsManager.saveItem('${type}', ${isEdit})">
                        <i class="fas ${icon}"></i> ${action}
                    </button>
                </div>
            </div>
        `;
    }

    getTypeLabel(type) {
        switch (type) {
            case 'document-type': return 'Tipo de Documento';
            case 'category': return 'Categoría';
            case 'client': return 'Cliente';
            default: return 'Elemento';
        }
    }

    getCurrentListContainer() {
        switch (this.currentTab) {
            case 'document-types': return document.getElementById('documentTypesList');
            case 'categories': return document.getElementById('categoriesList');
            case 'clients': return document.getElementById('clientsList');
            default: return null;
        }
    }

    async saveItem(type, isEdit) {
        const form = document.querySelector('.metadata-form');
        if (!form) return;

        const formData = this.getFormData(form, type);
        if (!formData) return;

        try {
            if (isEdit) {
                await this.updateItem(type, formData);
            } else {
                await this.createItem(type, formData);
            }
            
            this.removeForm(form);
            await this.loadTabContent(this.currentTab);
            notificationService.showSuccess(`${this.getTypeLabel(type)} ${isEdit ? 'actualizado' : 'creado'} exitosamente`);
        } catch (error) {
            console.error('Error saving item:', error);
            notificationService.showError(`Error al ${isEdit ? 'actualizar' : 'crear'} ${this.getTypeLabel(type).toLowerCase()}`);
        }
    }

    getFormData(form, type) {
        const name = form.querySelector('#name').value.trim();
        if (!name) {
            notificationService.showError('El nombre es obligatorio');
            return null;
        }

        const data = { name };
        
        if (type === 'client') {
            data.email = form.querySelector('#email').value.trim();
            data.phone = form.querySelector('#phone').value.trim();
        } else {
            data.description = form.querySelector('#description').value.trim();
        }

        if (form.dataset.id) {
            data.id = parseInt(form.dataset.id);
        }

        return data;
    }

    async createItem(type, data) {
        switch (type) {
            case 'document-type':
                await apiService.createDocumentType(data);
                break;
            case 'category':
                await apiService.createCategory(data);
                break;
            case 'client':
                await apiService.createClient(data);
                break;
        }
    }

    async updateItem(type, data) {
        switch (type) {
            case 'document-type':
                await apiService.updateDocumentType(data.id, data);
                break;
            case 'category':
                await apiService.updateCategory(data.id, data);
                break;
            case 'client':
                await apiService.updateClient(data.id, data);
                break;
        }
    }

    async deleteItem(id, type) {
        const confirmed = await uiService.confirm(`¿Estás seguro de que quieres eliminar este ${this.getTypeLabel(type).toLowerCase()}?`);
        if (!confirmed) {
            return;
        }

        try {
            switch (type) {
                case 'document-type':
                    await apiService.deleteDocumentType(id);
                    break;
                case 'category':
                    await apiService.deleteCategory(id);
                    break;
                case 'client':
                    await apiService.deleteClient(id);
                    break;
            }

            await this.loadTabContent(this.currentTab);
            notificationService.showSuccess(`${this.getTypeLabel(type)} eliminado exitosamente`);
        } catch (error) {
            console.error('Error deleting item:', error);
            notificationService.showError(`Error al eliminar ${this.getTypeLabel(type).toLowerCase()}`);
        }
    }

    cancelForm() {
        const form = document.querySelector('.metadata-form');
        if (form) {
            this.removeForm(form);
        }
    }

    removeForm(form) {
        form.remove();
    }

    resetForm() {
        const forms = document.querySelectorAll('.metadata-form');
        forms.forEach(form => form.remove());
        this.editingItem = null;
    }
}

// Export instance
export const settingsManager = new SettingsManagerService(); 