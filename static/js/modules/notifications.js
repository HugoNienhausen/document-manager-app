/**
 * Notifications Module
 * Maneja las notificaciones del sistema
 */

export class NotificationService {
    constructor() {
        this.container = document.getElementById('notifications');
        this.notifications = [];
        this.initializeContainer();
    }

    initializeContainer() {
        if (!this.container) {
            this.container = document.createElement('div');
            this.container.id = 'notifications';
            this.container.className = 'notifications';
            document.body.appendChild(this.container);
        }
    }

    show(message, type = 'info', duration = 5000) {
        const notification = this.createNotification(message, type);
        this.container.appendChild(notification);
        this.notifications.push(notification);

        // Animar entrada
        setTimeout(() => {
            notification.classList.add('show');
        }, 100);

        // Auto-remover después del tiempo especificado
        if (duration > 0) {
            setTimeout(() => {
                this.remove(notification);
            }, duration);
        }

        return notification;
    }

    showSuccess(message, duration = 5000) {
        return this.show(message, 'success', duration);
    }

    showError(message, duration = 8000) {
        return this.show(message, 'error', duration);
    }

    showWarning(message, duration = 6000) {
        return this.show(message, 'warning', duration);
    }

    showInfo(message, duration = 5000) {
        return this.show(message, 'info', duration);
    }

    createNotification(message, type) {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        
        const icon = this.getIconForType(type);
        
        notification.innerHTML = `
            <div class="notification-content">
                <div class="notification-icon">
                    <i class="${icon}"></i>
                </div>
                <div class="notification-message">
                    ${message}
                </div>
                <button class="notification-close" onclick="this.parentElement.parentElement.remove()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;

        // Agregar event listener para cerrar
        const closeBtn = notification.querySelector('.notification-close');
        closeBtn.addEventListener('click', () => {
            this.remove(notification);
        });

        return notification;
    }

    getIconForType(type) {
        switch (type) {
            case 'success':
                return 'fas fa-check-circle';
            case 'error':
                return 'fas fa-exclamation-circle';
            case 'warning':
                return 'fas fa-exclamation-triangle';
            case 'info':
            default:
                return 'fas fa-info-circle';
        }
    }

    remove(notification) {
        if (notification && notification.parentNode) {
            notification.classList.remove('show');
            notification.classList.add('hiding');
            
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
                const index = this.notifications.indexOf(notification);
                if (index > -1) {
                    this.notifications.splice(index, 1);
                }
            }, 300);
        }
    }

    clearAll() {
        this.notifications.forEach(notification => {
            this.remove(notification);
        });
    }
}

// Export instance
export const notificationService = new NotificationService(); 