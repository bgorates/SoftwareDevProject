/**
 * Application Configuration
 * Centralized configuration settings
 */

const CONFIG = {
    // API Configuration
    // Uses same origin when frontend is served by FastAPI
    // For separate development servers, set API_BASE_URL environment variable or update here
    API: {
        BASE_URL: window.location.origin, // Default: same origin (works when served by FastAPI)
        // BASE_URL: 'http://localhost:8000', // Uncomment for separate frontend/backend servers
        PREFIX: '',
        TIMEOUT: 30000, // 30 seconds
    },
    
    // Application Settings
    APP: {
        NAME: 'SlotMeIn',
        VERSION: '1.0.0',
        TITLE: 'SlotMeIn - Shift Scheduling System',
    },
    
    // Storage Keys
    STORAGE: {
        TOKEN: 'access_token',
        TOKEN_TYPE: 'token_type',
        USER_ROLE: 'user_role',
        LOGIN_TIME: 'login_time',
        REMEMBER_ME: 'remember_me',
    },
    
    // Routes
    ROUTES: {
        LOGIN: '/pages/auth/admin-login.html',
        SUPERUSER_LOGIN: '/pages/auth/superuser-login.html',
        DASHBOARD: '/pages/dashboard.html',
        SUPERUSER_DASHBOARD: '/pages/superuser/dashboard.html',
    },
    
    // Feature Flags
    FEATURES: {
        DARK_MODE: false,
        NOTIFICATIONS: true,
        ANALYTICS: false,
    }
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
}


