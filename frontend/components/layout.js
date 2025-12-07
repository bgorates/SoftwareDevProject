/**
 * Layout Component
 * Provides consistent page layout structure
 */

function createPageLayout(content, options = {}) {
    const {
        title = 'SlotMeIn',
        subtitle = '',
        showNavbar = true,
        navbarOptions = {},
        headerActions = ''
    } = options;

    return `
        ${showNavbar ? `<div id="navbar-container" data-brand-link="${navbarOptions.brandLink || 'dashboard.html'}"></div>` : ''}
        <div class="container">
            <div class="page-header">
                ${headerActions ? `
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <h1>${title}</h1>
                            ${subtitle ? `<p style="color: var(--text-secondary); margin-top: 8px;">${subtitle}</p>` : ''}
                        </div>
                        ${headerActions}
                    </div>
                ` : `
                    <h1>${title}</h1>
                    ${subtitle ? `<p style="color: var(--text-secondary); margin-top: 8px;">${subtitle}</p>` : ''}
                `}
            </div>
            ${content}
        </div>
    `;
}

// Helper function to set page title
function setPageTitle(title) {
    document.title = `${title} - SlotMeIn`;
}

// Helper function to create page header
function createPageHeader(title, subtitle = '', actions = '') {
    if (actions) {
        return `
            <div class="page-header">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h1>${title}</h1>
                        ${subtitle ? `<p style="color: var(--text-secondary); margin-top: 8px;">${subtitle}</p>` : ''}
                    </div>
                    ${actions}
                </div>
            </div>
        `;
    }
    return `
        <div class="page-header">
            <h1>${title}</h1>
            ${subtitle ? `<p style="color: var(--text-secondary); margin-top: 8px;">${subtitle}</p>` : ''}
        </div>
    `;
}


