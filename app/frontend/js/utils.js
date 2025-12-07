// Utility functions for the frontend

// Format date to YYYY-MM-DD
function formatDate(date) {
    if (!date) return '';
    const d = new Date(date);
    const year = d.getFullYear();
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

// Format time to HH:MM
function formatTime(time) {
    if (!time) return '';
    if (typeof time === 'string') {
        // Handle "HH:MM:SS" or "HH:MM" format
        return time.substring(0, 5);
    }
    return time;
}

// Format datetime
function formatDateTime(datetime) {
    if (!datetime) return '';
    const d = new Date(datetime);
    return d.toLocaleString();
}

// Show notification/toast
function showNotification(message, type = 'info', duration = 3000) {
    // Remove existing notifications
    const existing = document.querySelector('.notification');
    if (existing) {
        existing.remove();
    }
    
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Add styles
    Object.assign(notification.style, {
        position: 'fixed',
        top: '20px',
        right: '20px',
        padding: '12px 24px',
        borderRadius: '8px',
        color: 'white',
        fontWeight: '500',
        zIndex: '10000',
        boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
        animation: 'slideIn 0.3s ease-out',
    });
    
    // Set background color based on type
    const colors = {
        success: '#10B981',
        error: '#EF4444',
        warning: '#F59E0B',
        info: '#3B82F6',
    };
    notification.style.backgroundColor = colors[type] || colors.info;
    
    document.body.appendChild(notification);
    
    // Auto remove after duration
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, duration);
}

// Show loading spinner
function showLoading(element) {
    if (!element) return;
    
    const spinner = document.createElement('div');
    spinner.className = 'loading-spinner';
    spinner.innerHTML = `
        <svg class="spinner" width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="20" cy="20" r="16" stroke="#4F46E5" stroke-width="3" stroke-linecap="round" stroke-dasharray="50.27" stroke-dashoffset="50.27">
                <animate attributeName="stroke-dasharray" dur="2s" values="0 50.27;25.13 25.13;0 50.27;0 50.27" repeatCount="indefinite"/>
                <animate attributeName="stroke-dashoffset" dur="2s" values="0;-25.13;-50.27;-50.27" repeatCount="indefinite"/>
            </circle>
        </svg>
    `;
    
    Object.assign(spinner.style, {
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        padding: '20px',
    });
    
    element.appendChild(spinner);
    return spinner;
}

// Hide loading spinner
function hideLoading(spinner) {
    if (spinner && spinner.parentNode) {
        spinner.remove();
    }
}

// Debounce function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Validate email
function isValidEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Validate required fields
function validateRequired(fields) {
    const errors = {};
    for (const [key, value] of Object.entries(fields)) {
        if (!value || (typeof value === 'string' && !value.trim())) {
            errors[key] = `${key} is required`;
        }
    }
    return errors;
}

// Get week start date (Monday)
function getWeekStart(date = new Date()) {
    const d = new Date(date);
    const day = d.getDay();
    const diff = d.getDate() - day + (day === 0 ? -6 : 1); // Adjust when day is Sunday
    return new Date(d.setDate(diff));
}

// Format week range
function formatWeekRange(weekStart) {
    const start = new Date(weekStart);
    const end = new Date(start);
    end.setDate(end.getDate() + 6);
    
    return `${formatDate(start)} - ${formatDate(end)}`;
}

// Capitalize first letter
function capitalize(str) {
    if (!str) return '';
    return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
}

// Format role name
function formatRole(role) {
    if (!role) return '';
    // Handle both underscores and spaces, capitalize each word
    return role.split(/[_\s]+/).map(capitalize).join(' ');
}

// Confirm dialog
function confirmDialog(message, title = 'Confirm') {
    return new Promise((resolve) => {
        const dialog = document.createElement('div');
        dialog.className = 'confirm-dialog-overlay';
        dialog.innerHTML = `
            <div class="confirm-dialog">
                <h3>${title}</h3>
                <p>${message}</p>
                <div class="confirm-dialog-actions">
                    <button class="btn btn-secondary" data-action="cancel">Cancel</button>
                    <button class="btn btn-primary" data-action="confirm">Confirm</button>
                </div>
            </div>
        `;
        
        dialog.querySelector('[data-action="cancel"]').addEventListener('click', () => {
            dialog.remove();
            resolve(false);
        });
        
        dialog.querySelector('[data-action="confirm"]').addEventListener('click', () => {
            dialog.remove();
            resolve(true);
        });
        
        document.body.appendChild(dialog);
    });
}

// Add CSS for notifications and dialogs
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .confirm-dialog-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 10000;
    }
    
    .confirm-dialog {
        background: white;
        border-radius: 12px;
        padding: 24px;
        max-width: 400px;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
    }
    
    .confirm-dialog h3 {
        margin: 0 0 12px 0;
        font-size: 18px;
        font-weight: 600;
    }
    
    .confirm-dialog p {
        margin: 0 0 24px 0;
        color: #6B7280;
    }
    
    .confirm-dialog-actions {
        display: flex;
        gap: 12px;
        justify-content: flex-end;
    }
`;
document.head.appendChild(style);


