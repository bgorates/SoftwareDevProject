// API Configuration
// Automatically uses same origin when frontend is served by FastAPI
// If running separately, update this to backend URL (e.g., 'http://localhost:8000')
const API_BASE_URL = window.location.origin;
const API_PREFIX = ''; // FastAPI typically serves from root

// API Endpoints
const API_ENDPOINTS = {
    // Auth endpoints
    LOGIN: '/users/login_token',
    CREATE_USER: '/users/create',
    SEND_INVITE: '/users/send_invite',
    ACCEPT_INVITE: '/users/accept_invite',
    GET_INVITE: '/users/accept_invite',
    LIST_USERS: '/users/list',

    // Talent endpoints
    CREATE_TALENT: '/talents/create',
    UPDATE_TALENT: '/talents/update',
    GET_TALENTS: '/talents/retrieve_talents',
    GET_TALENT: '/talents/retrieve_talent',

    // Shift Template endpoints
    CREATE_TEMPLATE: '/shift_templates/create',
    UPDATE_TEMPLATE: '/shift_templates/update',
    DELETE_TEMPLATE: '/shift_templates/delete',
    GET_TEMPLATES: '/shift_templates/retrieve_all_templates',
    GET_TEMPLATE: '/shift_templates/retrieve_template',

    // Talent Constraints endpoints
    CREATE_CONSTRAINT: '/talent_constraints/create',
    DELETE_CONSTRAINT: '/talent_constraints/delete',
    GET_CONSTRAINTS: '/talent_constraints/retrieve_all_constraints',
    GET_CONSTRAINT: '/talent_constraints/retrieve_constraint',

    // Constraint Rules endpoints
    CREATE_CONSTRAINT_RULE: '/constraint_rules/create',
    DELETE_CONSTRAINT_RULE: '/constraint_rules/delete',

    // Shift Period endpoints
    GET_PERIODS: '/shift_period/retrieve_all_periods',
    GET_PERIOD: '/shift_period/retrieve_period',

    // Schedule endpoints
    GENERATE_SCHEDULE: '/schedule/generate',
    VIEW_SCHEDULE: '/schedule/view',
};

// Get stored token
function getAuthToken() {
    return localStorage.getItem('access_token') || sessionStorage.getItem('access_token');
}

// Get stored user role
function getUserRole() {
    return localStorage.getItem('user_role') || sessionStorage.getItem('user_role');
}

// Build full URL
function buildUrl(endpoint, params = {}) {
    let url = `${API_BASE_URL}${API_PREFIX}${endpoint}`;

    // Add query parameters
    const queryString = Object.keys(params)
        .filter(key => params[key] !== null && params[key] !== undefined)
        .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(params[key])}`)
        .join('&');

    if (queryString) {
        url += `?${queryString}`;
    }

    return url;
}

// Make API request
async function apiRequest(endpoint, options = {}) {
    const token = getAuthToken();
    const url = buildUrl(endpoint, options.params);

    const defaultHeaders = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    };

    if (token) {
        defaultHeaders['Authorization'] = `Bearer ${token}`;
    }

    const config = {
        ...options,
        headers: {
            ...defaultHeaders,
            ...options.headers,
        },
    };

    // Remove Content-Type for FormData
    if (options.body instanceof FormData) {
        delete config.headers['Content-Type'];
    }

    try {
        console.log('Making API request to:', url); // Debug log
        const response = await fetch(url, config);
        console.log('Response status:', response.status); // Debug log

        // Handle non-JSON responses and 204 No Content
        const contentType = response.headers.get('content-type');
        let data;

        // For 204 No Content, there's no response body - return empty object
        if (response.status === 204) {
            data = {};
        } else if (contentType && contentType.includes('application/json')) {
            try {
                const text = await response.text();
                // Only parse JSON if there's actual content
                if (text && text.trim()) {
                    data = JSON.parse(text);
                } else {
                    data = {};
                }
            } catch (e) {
                // If JSON parsing fails (e.g., empty or invalid JSON), return empty object
                console.warn('Failed to parse JSON response:', e);
                data = {};
            }
        } else {
            const text = await response.text();
            data = text ? { detail: text } : {};
        }

        if (!response.ok) {
            // Handle 401 Unauthorized
            if (response.status === 401) {
                const isLoginPage = window.location.pathname.includes('/admin-login.html') ||
                    window.location.pathname.includes('/login.html') ||
                    window.location.pathname.includes('/superuser-login.html') ||
                    window.location.pathname.includes('/pages/auth/admin-login.html') ||
                    window.location.pathname.includes('/pages/auth/login.html') ||
                    window.location.pathname.includes('/pages/auth/superuser-login.html');

                // If on login page, show the error message (don't redirect)
                if (isLoginPage) {
                    const errorMessage = data.detail || data.message || 'Invalid username or password';
                    console.log('Login page 401 error:', errorMessage); // Debug log
                    throw new Error(errorMessage);
                }

                // Otherwise, redirect to login
                clearAuth();
                throw new Error('Unauthorized. Please login again.');
            }

            // For 500 errors, try to get more details
            // Handle validation errors (422) - show detailed field errors
            if (response.status === 422 && data.detail) {
                let errorMsg = 'Validation error: ';
                if (Array.isArray(data.detail)) {
                    // FastAPI validation errors are arrays
                    const fieldErrors = data.detail.map(err => {
                        const field = err.loc ? err.loc.join('.') : 'field';
                        return `${field}: ${err.msg}`;
                    }).join(', ');
                    errorMsg += fieldErrors;
                } else if (typeof data.detail === 'string') {
                    errorMsg += data.detail;
                } else {
                    errorMsg += JSON.stringify(data.detail);
                }
                console.error('Validation error details:', data);
                throw new Error(errorMsg);
            }

            const errorMessage = data.detail || data.message || `Request failed with status ${response.status}`;
            console.error('Server error details:', data); // Log full error response
            throw new Error(errorMessage);
        }

        return data;
    } catch (error) {
        console.error('API request error:', error);
        console.error('Request URL:', url);
        console.error('Error type:', error.constructor.name);
        console.error('Error message:', error.message);

        // Handle network errors
        if (error instanceof TypeError && (error.message.includes('fetch') || error.message.includes('Failed to fetch'))) {
            throw new Error('Unable to connect to server. Please check if the API is running at ' + url + '. Make sure you started the server with: python run_server.py');
        }
        // Handle other errors
        if (error.name === 'NetworkError' || error.message.includes('network')) {
            throw new Error('Network error. Please check your internet connection and ensure the server is running.');
        }
        throw error;
    }
}

// API Methods
const api = {
    // Auth methods
    login: async (username, password) => {
        const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);

        return apiRequest(API_ENDPOINTS.LOGIN, {
            method: 'POST',
            body: formData,
        });
    },

    createUser: async (userData) => {
        return apiRequest(API_ENDPOINTS.CREATE_USER, {
            method: 'POST',
            body: JSON.stringify(userData),
        });
    },

    sendInvite: async (userId) => {
        return apiRequest(API_ENDPOINTS.SEND_INVITE, {
            method: 'POST',
            body: JSON.stringify({ user_id: userId }),
        });
    },

    acceptInvite: async (token, newPassword) => {
        return apiRequest(API_ENDPOINTS.ACCEPT_INVITE, {
            method: 'POST',
            body: JSON.stringify({ token, new_password: newPassword }),
        });
    },

    getInvite: async (token) => {
        return apiRequest(API_ENDPOINTS.GET_INVITE, {
            method: 'GET',
            params: { token },
        });
    },

    listUsers: async (role = null) => {
        const url = role
            ? `${API_ENDPOINTS.LIST_USERS}?role=${encodeURIComponent(role)}`
            : API_ENDPOINTS.LIST_USERS;
        return apiRequest(url, {
            method: 'GET',
        });
    },

    // Talent methods
    createTalent: async (talentData) => {
        return apiRequest(API_ENDPOINTS.CREATE_TALENT, {
            method: 'POST',
            body: JSON.stringify(talentData),
        });
    },

    updateTalent: async (talentId, talentData) => {
        return apiRequest(`${API_ENDPOINTS.UPDATE_TALENT}/${talentId}`, {
            method: 'PUT',
            body: JSON.stringify(talentData),
        });
    },

    getTalents: async (filters = {}) => {
        return apiRequest(API_ENDPOINTS.GET_TALENTS, {
            method: 'GET',
            params: filters,
        });
    },

    getTalent: async (talentId) => {
        return apiRequest(`${API_ENDPOINTS.GET_TALENT}/${talentId}`, {
            method: 'GET',
        });
    },

    // Shift Template methods
    createTemplate: async (templateData) => {
        return apiRequest(API_ENDPOINTS.CREATE_TEMPLATE, {
            method: 'POST',
            body: JSON.stringify(templateData),
        });
    },

    updateTemplate: async (templateId, templateData) => {
        return apiRequest(`${API_ENDPOINTS.UPDATE_TEMPLATE}/${templateId}`, {
            method: 'PUT',
            body: JSON.stringify(templateData),
        });
    },

    deleteTemplate: async (templateId) => {
        return apiRequest(`${API_ENDPOINTS.DELETE_TEMPLATE}/${templateId}`, {
            method: 'DELETE',
        });
    },

    getTemplates: async (filters = {}) => {
        return apiRequest(API_ENDPOINTS.GET_TEMPLATES, {
            method: 'GET',
            params: filters,
        });
    },

    getTemplate: async (templateId) => {
        return apiRequest(`${API_ENDPOINTS.GET_TEMPLATE}/${templateId}`, {
            method: 'GET',
        });
    },

    // Constraint methods
    createConstraint: async (constraintData) => {
        return apiRequest(API_ENDPOINTS.CREATE_CONSTRAINT, {
            method: 'POST',
            body: JSON.stringify(constraintData),
        });
    },

    deleteConstraint: async (constraintId) => {
        return apiRequest(`${API_ENDPOINTS.DELETE_CONSTRAINT}/${constraintId}`, {
            method: 'DELETE',
        });
    },

    // Constraint Rule methods
    createConstraintRule: async (ruleData) => {
        return apiRequest(API_ENDPOINTS.CREATE_CONSTRAINT_RULE, {
            method: 'POST',
            body: JSON.stringify(ruleData),
        });
    },

    deleteConstraintRule: async (ruleId) => {
        return apiRequest(`${API_ENDPOINTS.DELETE_CONSTRAINT_RULE}/${ruleId}`, {
            method: 'DELETE',
        });
    },

    getConstraints: async (filters = {}) => {
        return apiRequest(API_ENDPOINTS.GET_CONSTRAINTS, {
            method: 'GET',
            params: filters,
        });
    },

    getConstraint: async (constraintId) => {
        return apiRequest(`${API_ENDPOINTS.GET_CONSTRAINT}/${constraintId}`, {
            method: 'GET',
        });
    },

    // Shift Period methods
    getPeriods: async (filters = {}) => {
        return apiRequest(API_ENDPOINTS.GET_PERIODS, {
            method: 'GET',
            params: filters,
        });
    },

    getPeriod: async (periodId) => {
        return apiRequest(`${API_ENDPOINTS.GET_PERIOD}/${periodId}`, {
            method: 'GET',
        });
    },

    // Schedule methods
    generateSchedule: async (startDate) => {
        return apiRequest(API_ENDPOINTS.GENERATE_SCHEDULE, {
            method: 'POST',
            body: JSON.stringify({ start_date: startDate }),
        });
    },

    getSchedules: async () => {
        return apiRequest('/schedule/list', {
            method: 'GET',
        });
    },

    getScheduleByWeek: async (weekStart) => {
        return apiRequest(`/schedule/week/${weekStart}`, {
            method: 'GET',
        });
    },

    viewSchedule: async (weekStart) => {
        return apiRequest(`${API_ENDPOINTS.VIEW_SCHEDULE}/${weekStart}`, {
            method: 'GET',
        });
    },
};

// Clear authentication
function clearAuth() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('token_type');
    localStorage.removeItem('user_role');
    localStorage.removeItem('login_time');
    sessionStorage.removeItem('access_token');
    sessionStorage.removeItem('token_type');
    sessionStorage.removeItem('user_role');
    sessionStorage.removeItem('login_time');
}

// Check if user is authenticated
function isAuthenticated() {
    return !!getAuthToken();
}

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { api, getAuthToken, getUserRole, clearAuth, isAuthenticated };
}

