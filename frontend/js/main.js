/**
 * Main Application Script
 * Initializes the application and sets up global functionality
 */

// Initialize application when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

/**
 * Initialize the application
 */
function initializeApp() {
    // Set up global error handler
    window.addEventListener('error', handleGlobalError);
    window.addEventListener('unhandledrejection', handleUnhandledRejection);
    
    // Initialize authentication check
    checkAuthentication();
    
    // Initialize components
    initializeComponents();
}

/**
 * Handle global errors
 */
function handleGlobalError(event) {
    console.error('Global error:', event.error);
    // You can add error reporting here
}

/**
 * Handle unhandled promise rejections
 */
function handleUnhandledRejection(event) {
    console.error('Unhandled rejection:', event.reason);
    // You can add error reporting here
}

/**
 * Check authentication status
 */
function checkAuthentication() {
    // This will be handled by individual pages
    // Pages that require auth should check isAuthenticated()
}

/**
 * Initialize components
 */
function initializeComponents() {
    // Initialize navbar if container exists
    if (document.getElementById('navbar-container')) {
        // Navbar will auto-initialize via navbar.js
    }
    
    // Add any other global component initialization here
}

/**
 * Global logout function
 */
function logout() {
    if (confirm('Are you sure you want to logout?')) {
        if (typeof clearAuth === 'function') {
            clearAuth();
        }
        const userRole = typeof getUserRole === 'function' ? getUserRole() : null;
        if (typeof CONFIG !== 'undefined' && CONFIG.ROUTES) {
            if (userRole === 'superuser') {
                window.location.href = CONFIG.ROUTES.SUPERUSER_LOGIN;
            } else {
                window.location.href = CONFIG.ROUTES.LOGIN;
            }
        } else {
            // Fallback if CONFIG not loaded
            window.location.href = '/pages/auth/admin-login.html';
        }
    }
}

// Make logout available globally
window.logout = logout;

