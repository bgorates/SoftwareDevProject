/**
 * Navbar Component
 * Reusable navigation bar for authenticated pages
 */

function createNavbar(options = {}) {
    const {
        brand = 'SlotMeIn',
        brandLink = '/pages/employees/dashboard.html',
        items = [],
        actions = [],
        userRole = getUserRole()
    } = options;

    // No default navigation items - only brand and logout
    const navItems = items.length > 0 ? items : [];
    const navActions = actions.length > 0 ? actions : [
        { label: 'Logout', onclick: 'logout()', class: 'btn-secondary btn-sm' }
    ];

    return `
        <nav class="navbar">
            <div class="navbar-content">
                <a href="${brandLink}" class="navbar-brand">${brand}</a>
                ${navItems.length > 0 ? `
                <ul class="navbar-nav">
                    ${navItems.map(item => 
                        `<li><a href="${item.href}">${item.label}</a></li>`
                    ).join('')}
                </ul>
                ` : ''}
                <div class="navbar-actions">
                    ${navActions.map(action => 
                        action.href 
                            ? `<a href="${action.href}" class="btn ${action.class || ''}">${action.label}</a>`
                            : `<button class="btn ${action.class || ''}" onclick="${action.onclick}">${action.label}</button>`
                    ).join('')}
                </div>
            </div>
        </nav>
    `;
}

// Auto-inject navbar if navbar-container exists
document.addEventListener('DOMContentLoaded', () => {
    const navbarContainer = document.getElementById('navbar-container');
    if (navbarContainer) {
        // Get user role to determine correct dashboard
        const userRole = getUserRole();
        
        // Use absolute path to dashboard from frontend root
        const defaultEmployeeDashboard = '/pages/employees/dashboard.html';
        const defaultSuperuserDashboard = '/pages/superuser/superuser-dashboard.html';
        
        let brandLink = navbarContainer.dataset.brandLink || defaultEmployeeDashboard;
        
        // Convert relative "dashboard.html" to absolute path based on user role
        if (brandLink === 'dashboard.html') {
            // If user is superuser, redirect to superuser dashboard
            // Otherwise, redirect to employee dashboard
            brandLink = (userRole === 'superuser') 
                ? defaultSuperuserDashboard 
                : defaultEmployeeDashboard;
        }
        
        const options = {
            brandLink: brandLink,
            userRole: userRole
        };
        navbarContainer.innerHTML = createNavbar(options);
    }
});

