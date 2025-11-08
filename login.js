// Configuration - Update this with your API base URL
const API_BASE_URL = 'http://localhost:8000';
const LOGIN_ENDPOINT = `${API_BASE_URL}/users/login_token`;

// DOM Elements
const loginForm = document.getElementById('loginForm');
const usernameInput = document.getElementById('username');
const passwordInput = document.getElementById('password');
const togglePasswordBtn = document.getElementById('togglePassword');
const loginButton = document.getElementById('loginButton');
const errorMessage = document.getElementById('errorMessage');
const successMessage = document.getElementById('successMessage');
const rememberMeCheckbox = document.getElementById('rememberMe');

// Toggle password visibility
togglePasswordBtn.addEventListener('click', () => {
    const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordInput.setAttribute('type', type);
    
    // Update icon (simple toggle - you can enhance this with different icons)
    const icon = togglePasswordBtn.querySelector('svg');
    if (type === 'text') {
        icon.innerHTML = `
            <path d="M10 12.5C8.62 12.5 7.5 11.38 7.5 10C7.5 9.4 7.73 8.85 8.1 8.45L11.55 11.9C11.15 12.27 10.6 12.5 10 12.5ZM12.45 9.55L9 6.1C9.4 5.73 9.95 5.5 10.5 5.5C11.88 5.5 13 6.62 13 8C13 8.55 12.77 9.1 12.45 9.55ZM2 4.27L4.28 6.55L4.73 7H2V9H4.18C4.06 9.32 4 9.65 4 10C4 11.1 4.9 12 6 12H8.18L10.18 14H6C3.79 14 2 12.21 2 10V6C2 5.5 2.23 5.05 2.59 4.73L1.27 3.41L2.68 2L17.73 17.05L16.32 18.46L2 4.27ZM16 6H14.82C14.94 5.68 15 5.35 15 5C15 3.9 14.1 3 13 3H11C9.9 3 9 3.9 9 5C9 5.03 9 5.07 9.01 5.1L16 12.09V6Z" fill="#6B7280"/>
        `;
    } else {
        icon.innerHTML = `
            <path d="M10 4C6 4 3.27 6.11 2 9C3.27 11.89 6 14 10 14C14 14 16.73 11.89 18 9C16.73 6.11 14 4 10 4ZM10 12C8.34 12 7 10.66 7 9C7 7.34 8.34 6 10 6C11.66 6 13 7.34 13 9C13 10.66 11.66 12 10 12ZM10 7.5C9.17 7.5 8.5 8.17 8.5 9C8.5 9.83 9.17 10.5 10 10.5C10.83 10.5 11.5 9.83 11.5 9C11.5 8.17 10.83 7.5 10 7.5Z" fill="#6B7280"/>
        `;
    }
});

// Show error message
function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'flex';
    successMessage.style.display = 'none';
    errorMessage.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Show success message
function showSuccess(message) {
    successMessage.textContent = message;
    successMessage.style.display = 'flex';
    errorMessage.style.display = 'none';
}

// Hide all messages
function hideMessages() {
    errorMessage.style.display = 'none';
    successMessage.style.display = 'none';
}

// Set loading state
function setLoading(loading) {
    loginButton.disabled = loading;
    const buttonText = loginButton.querySelector('.button-text');
    const buttonLoader = loginButton.querySelector('.button-loader');
    
    if (loading) {
        buttonText.style.display = 'none';
        buttonLoader.style.display = 'flex';
    } else {
        buttonText.style.display = 'inline';
        buttonLoader.style.display = 'none';
    }
}

// Store token in localStorage or sessionStorage
function storeToken(token, role) {
    const storage = rememberMeCheckbox.checked ? localStorage : sessionStorage;
    storage.setItem('access_token', token);
    storage.setItem('token_type', 'bearer');
    storage.setItem('user_role', role);
    storage.setItem('login_time', new Date().toISOString());
}

// Handle form submission
loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    hideMessages();
    setLoading(true);

    const username = usernameInput.value.trim();
    const password = passwordInput.value;

    // Basic validation
    if (!username || !password) {
        showError('Please enter both username and password');
        setLoading(false);
        return;
    }

    try {
        // Create FormData for OAuth2PasswordRequestForm
        const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);

        // Make API request
        const response = await fetch(LOGIN_ENDPOINT, {
            method: 'POST',
            body: formData,
            headers: {
                'Accept': 'application/json',
            }
        });

        const data = await response.json();

        if (!response.ok) {
            // Handle error response
            const errorDetail = data.detail || 'Login failed. Please check your credentials.';
            showError(errorDetail);
            setLoading(false);
            return;
        }

        // Success - store token and redirect
        if (data.access_token) {
            storeToken(data.access_token, data.role);
            showSuccess(`Login successful! Welcome, ${data.role}. Redirecting...`);
            
            // Redirect to dashboard or home page after a short delay
            setTimeout(() => {
                // You can change this to redirect to your dashboard
                window.location.href = 'dashboard.html'; // or wherever you want to redirect
            }, 1500);
        } else {
            showError('Invalid response from server');
            setLoading(false);
        }

    } catch (error) {
        console.error('Login error:', error);
        
        // Handle network errors
        if (error instanceof TypeError && error.message.includes('fetch')) {
            showError('Unable to connect to server. Please check if the API is running.');
        } else {
            showError('An unexpected error occurred. Please try again.');
        }
        setLoading(false);
    }
});

// Clear error on input
usernameInput.addEventListener('input', hideMessages);
passwordInput.addEventListener('input', hideMessages);

// Enter key handling (already handled by form submit, but for accessibility)
passwordInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        loginForm.dispatchEvent(new Event('submit'));
    }
});

// Check if user is already logged in (optional)
window.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('access_token') || sessionStorage.getItem('access_token');
    if (token) {
        // User is already logged in, you might want to redirect them
        // window.location.href = 'dashboard.html';
    }
});

