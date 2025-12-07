# Frontend Structure

This document describes the organized structure of the SlotMeIn frontend application.

## Directory Structure

```
frontend/
├── index.html                 # Entry point / Welcome page
├── README.md                  # Frontend documentation
├── STRUCTURE.md              # This file
│
├── assets/                    # Static assets
│   └── images/                # Image files
│
├── components/                # Reusable components
│   ├── navbar.js             # Navigation bar component
│   └── layout.js             # Layout helper functions
│
├── css/                       # Stylesheets
│   ├── main.css              # Main stylesheet (imports all modules)
│   ├── login.css             # Login page specific styles (in pages/auth/)
│   └── modules/              # CSS modules
│       ├── variables.css     # CSS variables / design tokens
│       ├── base.css          # Base styles, reset, typography
│       └── components.css    # Reusable component styles
│
├── js/                        # JavaScript files
│   ├── main.js               # Application initialization
│   ├── config.js             # Configuration settings
│   ├── api.js                # API client and endpoints
│   ├── utils.js              # Utility functions
│   └── modules/              # Additional JS modules (future)
│
└── pages/                     # Page files organized by feature
    ├── auth/                  # Authentication pages
    │   ├── login.html
    │   ├── login.js
    │   ├── login.css
    │   ├── superuser-login.html
    │   └── reset-password.html
    │
    ├── superuser/             # Superuser pages
    │   ├── dashboard.html
    │   ├── create-business-account.html
    │   ├── manage-accounts.html
    │   └── pending-invitations.html
    │
    ├── employees/              # Employee management pages
    │   ├── dashboard.html
    │   ├── employee-list.html
    │   ├── employee-edit.html
    │   └── employee-constraints.html
    │
    ├── shifts/                 # Shift template pages
    │   ├── shift-template-list.html
    │   └── shift-template-edit.html
    │
    └── schedules/              # Schedule pages
        ├── schedule-generation.html
        ├── schedule-draft.html
        ├── schedule-published.html
        └── schedule-history.html
```

## Path Conventions

### From pages/ subdirectories:
- CSS: `../../css/main.css`
- JS: `../../js/[filename].js`
- Components: `../../components/[filename].js`
- Other pages: Relative paths like `../employees/dashboard.html`

### From root (index.html):
- CSS: `css/main.css`
- JS: `js/[filename].js`
- Pages: `pages/[category]/[page].html`

## File Naming Conventions

- **HTML files**: kebab-case (e.g., `employee-list.html`)
- **JavaScript files**: kebab-case (e.g., `api.js`, `login.js`)
- **CSS files**: kebab-case (e.g., `main.css`, `login.css`)
- **Component files**: kebab-case (e.g., `navbar.js`)

## Component Usage

### Navbar Component
```html
<div id="navbar-container" data-brand-link="dashboard.html"></div>
<script src="../../components/navbar.js"></script>
```

### Layout Helper
```javascript
import { createPageHeader } from '../../components/layout.js';
```

## CSS Architecture

1. **Variables** (`modules/variables.css`): Design tokens, colors, spacing
2. **Base** (`modules/base.css`): Reset, typography, base elements
3. **Components** (`modules/components.css`): Reusable UI components
4. **Main** (`main.css`): Imports all modules

## JavaScript Architecture

1. **Config** (`config.js`): Application configuration
2. **API** (`api.js`): API client and endpoints
3. **Utils** (`utils.js`): Utility functions
4. **Main** (`main.js`): Application initialization
5. **Components**: Reusable component scripts

## Best Practices

1. **Keep pages organized by feature** in the `pages/` directory
2. **Use relative paths** from the page location
3. **Import CSS modules** through `main.css` for consistency
4. **Use shared components** for common UI elements
5. **Follow naming conventions** for consistency
6. **Keep styles modular** - page-specific styles in page files or separate CSS files

## Adding New Pages

1. Create the HTML file in the appropriate `pages/[category]/` directory
2. Use the standard structure with navbar container
3. Import required CSS and JS files using relative paths
4. Follow the existing patterns for consistency

## Migration Notes

- All HTML files have been moved to `pages/` subdirectories
- CSS and JS paths have been updated to use relative paths
- Shared components are in the `components/` directory
- CSS has been modularized into separate files


