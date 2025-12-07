# SlotMeIn Frontend

Professional, well-structured frontend implementation for the SlotMeIn shift scheduling system.

## 📁 Project Structure

```
frontend/
├── index.html                 # Entry point / Welcome page
├── README.md                  # This file
├── STRUCTURE.md              # Detailed structure documentation
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
│   └── modules/              # CSS modules
│       ├── variables.css     # CSS variables / design tokens
│       ├── base.css          # Base styles, reset, typography
│       └── components.css    # Reusable component styles
│
├── js/                        # JavaScript files
│   ├── main.js               # Application initialization
│   ├── config.js             # Configuration settings
│   ├── api.js                # API client and endpoints
│   └── utils.js              # Utility functions
│
└── pages/                     # Page files organized by feature
    ├── auth/                  # Authentication pages
    ├── superuser/             # Superuser pages
    ├── employees/             # Employee management pages
    ├── shifts/                # Shift template pages
    └── schedules/             # Schedule pages
```

## 🎨 Architecture

### CSS Architecture (Modular)
- **Variables**: Design tokens, colors, spacing, typography
- **Base**: Reset, typography, base element styles
- **Components**: Reusable UI components (buttons, forms, tables, etc.)
- **Main**: Imports all modules for easy inclusion

### JavaScript Architecture
- **Config**: Centralized application configuration
- **API**: API client with authentication and error handling
- **Utils**: Utility functions (date formatting, validation, etc.)
- **Main**: Application initialization and global setup
- **Components**: Reusable component scripts

### Component System
- **Navbar**: Auto-initializing navigation component
- **Layout**: Helper functions for consistent page layouts

## 🚀 Getting Started

### 1. File Paths

**From `pages/[category]/` directories:**
```html
<!-- CSS -->
<link rel="stylesheet" href="../../css/main.css">

<!-- JavaScript (load in this order) -->
<script src="../../js/config.js"></script>
<script src="../../js/api.js"></script>
<script src="../../js/utils.js"></script>
<script src="../../js/main.js"></script>
<script src="../../components/navbar.js"></script>
```

**From root (`index.html`):**
```html
<link rel="stylesheet" href="css/main.css">
<script src="js/main.js"></script>
```

**Navigation Links:**
- Same directory: `page.html`
- Different category: `../employees/dashboard.html`
- Auth pages: `../auth/login.html`

### 2. Using Components

#### Navbar Component
```html
<div id="navbar-container" data-brand-link="dashboard.html"></div>
<script src="../../components/navbar.js"></script>
```

The navbar will automatically initialize based on the user's role.

#### Layout Helpers
```javascript
// Available in layout.js
createPageHeader(title, subtitle, actions);
setPageTitle(title);
```

## 📄 Pages Overview

### Authentication (`pages/auth/`)
- `login.html` - User login
- `superuser-login.html` - Superuser login
- `reset-password.html` - Account activation

### Superuser (`pages/superuser/`)
- `dashboard.html` - Superuser dashboard
- `create-business-account.html` - Create restaurant accounts
- `manage-accounts.html` - Manage all accounts
- `pending-invitations.html` - Manage invitations

### Employees (`pages/employees/`)
- `dashboard.html` - User dashboard
- `employee-list.html` - Employee management
- `employee-edit.html` - Create/edit employees
- `employee-constraints.html` - Set constraints

### Shifts (`pages/shifts/`)
- `shift-template-list.html` - View templates
- `shift-template-edit.html` - Create/edit templates

### Schedules (`pages/schedules/`)
- `schedule-generation.html` - Generate schedules
- `schedule-draft.html` - Editable draft
- `schedule-published.html` - Published view
- `schedule-history.html` - View history

## 🔧 Configuration

### API Configuration
Edit `js/config.js` to configure:
- API base URL
- Application settings
- Storage keys
- Feature flags

### Styling
Edit `css/modules/variables.css` to customize:
- Colors
- Spacing
- Typography
- Shadows
- Border radius

## 📝 Best Practices

1. **Organize by Feature**: Keep related pages in the same directory
2. **Use Relative Paths**: Always use relative paths from the current file location
3. **Import CSS Modules**: Use `main.css` which imports all modules
4. **Reuse Components**: Use shared components for common UI elements
5. **Follow Naming**: Use kebab-case for all file names
6. **Modular CSS**: Keep page-specific styles separate or in the page file

## 🔗 Navigation

### Internal Links
Use relative paths based on file location:
- Same directory: `employee-edit.html`
- Parent directory: `../employees/dashboard.html`
- Root pages: `../../pages/auth/login.html`

### External Links
Use absolute paths or full URLs for external resources.

## 🎯 Features

- ✅ Modular CSS architecture
- ✅ Component-based JavaScript
- ✅ Centralized API client
- ✅ Authentication handling
- ✅ Responsive design
- ✅ Clean, professional UI
- ✅ Well-organized structure
- ✅ Easy to maintain and extend

## 📚 Documentation

- **README.md** (this file) - Overview and quick reference
- **STRUCTURE.md** - Detailed directory structure and conventions
- Inline code comments - API usage and examples
- Component files - Usage examples in component source

## 🛠️ Development

### Adding a New Page

1. Create HTML file in appropriate `pages/[category]/` directory
2. Include standard structure:
   ```html
   <link rel="stylesheet" href="../../css/main.css">
   <div id="navbar-container"></div>
   <script src="../../components/navbar.js"></script>
   <script src="../../js/config.js"></script>
   <script src="../../js/api.js"></script>
   <script src="../../js/utils.js"></script>
   <script src="../../js/main.js"></script>
   ```
3. Follow existing patterns for consistency

### Adding a New Component

1. Create component file in `components/` directory
2. Export functions or use global scope
3. Document usage in component file
4. Update this README if needed

## 📦 Dependencies

- Modern browser (ES6+ support)
- Backend API (FastAPI)
- No external dependencies required

## 🔐 Authentication

- Tokens stored in localStorage/sessionStorage
- Automatic token inclusion in API requests
- Role-based navigation
- Auto-redirect on 401 errors

## 🎨 Styling

The application uses CSS custom properties (variables) for theming. All design tokens are defined in `css/modules/variables.css`.

### Color System
- Primary: `--primary-color`
- Success: `--success-color`
- Error: `--error-color`
- Warning: `--warning-color`
- Info: `--info-color`

### Spacing
- Uses consistent spacing scale: `--spacing-xs` through `--spacing-2xl`

### Typography
- Font family: System font stack
- Sizes: `--font-size-xs` through `--font-size-3xl`
- Weights: Normal, Medium, Semibold, Bold

## 📱 Responsive Design

The application is fully responsive with mobile-first approach:
- Breakpoints defined in component CSS
- Flexible grid layouts
- Mobile-optimized navigation
- Touch-friendly interactions

## 🚨 Error Handling

- Global error handlers in `main.js`
- API error handling in `api.js`
- User-friendly error messages
- Automatic retry for network errors (optional)

## 📈 Future Enhancements

- [ ] Dark mode support
- [ ] PWA capabilities
- [ ] Offline support
- [ ] Advanced animations
- [ ] Component library expansion
- [ ] Testing framework integration

---

**Note**: This frontend is designed to work with the SlotMeIn FastAPI backend. Ensure the backend is running and properly configured before use.
