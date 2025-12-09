# SlotMeIn

**SlotMeIn** is a FastAPI-based shift scheduling REST API designed to intelligently allocate employees (called **talents**) to shifts while respecting their availability, constraints, and labor regulations.

The system provides a complete backend solution with authentication, database management, and a sophisticated scheduling engine that ensures fair and compliant shift assignments.

> ⚠️ **Note:** This is an MVP and not yet in production.

---

## ✨ Current Features  

### 🔐 Authentication & User Management
- **JWT-based authentication**: Secure token-based authentication system
- **User management**: User registration and authentication endpoints

### 📊 RESTful API Endpoints
- **Talents Management** (`/talents`): CRUD operations for employee records
- **Shift Templates** (`/shift_templates`): Define shift patterns and roles
- **Shift Periods** (`/shift_period`): Manage shift time periods
- **Talent Constraints** (`/talent_constraints`): Configure employee availability constraints
- **Constraint Rules** (`/constraint_rules`): Define specific constraint rules per talent
- **Schedule Generation** (`/schedule/generate`): Generate optimized weekly schedules

### 🧠 Intelligent Scheduling Engine
- **Role & availability matching**: Filters talents based on role requirements, availability windows, and allowed shift types
- **Constraint validation**: Enforces labor regulations and business rules:
  - **Maximum weekly hours**: Respects individual talent weekly hour limits
  - **Daily assignment limit**: No more than one shift per day per talent
  - **Rest period enforcement**: Minimum 11 hours rest between consecutive shifts
  - **Consecutive workday limit**: Maximum six consecutive workdays
- **Smart prioritization**: 
  - Prioritizes constrained talents first, then unconstrained talents
  - Uses `computeScore` to evaluate talent suitability for each shift
  - Implements `roundRobinPicker` for fair distribution among equally-scored candidates
- **Quota-aware allocation**: Assigns the exact number of required talents per role/shift
- **Understaffing detection**: Identifies and reports shifts that couldn't be fully staffed

### 💾 Database Architecture
- **SQLAlchemy ORM**: Type-safe database models with relationships
- **PostgreSQL backend**: Robust relational database with connection pooling
- **Comprehensive data models**:
  - `Talent`: Employee records with roles and contract details
  - `TalentConstraint`: Availability constraints per talent
  - `ConstraintRule`: Specific rules defining when talents can work
  - `ShiftPeriod`: Shift time definitions
  - `ShiftTemplate`: Role-specific shift templates
  - `ScheduledShift`: Generated shift assignments
  - `Schedule`: Weekly schedule containers
  - `Request`: Time-off and preference requests

## 🚀 Future Enhancements  

- **Request handling**: Process and integrate time-off requests and preferences into scheduling
- **Advanced optimization**: Implement fairness metrics and workload balancing algorithms
- **Predictive staffing**: AI/ML models to forecast staffing needs based on demand patterns and seasonality
- **Shift swapping**: Allow talents to trade shifts with approval workflows

---

## 🛠️ Tech Stack

- **Backend Framework**: FastAPI 0.116+
- **Language**: Python 3.11+
- **Database**: SQLite (development) / PostgreSQL (production) with SQLAlchemy
- **ORM**: SQLAlchemy 2.0+
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt via passlib
- **Data Processing**: Pandas
- **API Documentation**: Auto-generated OpenAPI (Swagger UI)
- **Version Control**: Git

## 📁 Project Structure

```
Scheduler App/
├── frontend/                 # Frontend Application (HTML/JS)
│   ├── index.html            # Entry Point
│   ├── css/                  # Global Styles
│   ├── js/                   # Application Logic
│   └── pages/                # View Templates
│
├── backend/                  # Backend Application (FastAPI)
│   ├── authentication/       # JWT Auth & Security
│   ├── config/               # Environment Configuration
│   ├── core/                 # Core Domain Logic
│   │   ├── constraints/      # Constraint Rules & Validators
│   │   ├── schedule/         # Scheduling Engine
│   │   │   ├── allocator/    # Genetic Algorithm & Scoring
│   │   │   └── shifts/       # Shift Definition Logic
│   │   ├── talents/          # Staff Management Logic
│   │   └── utils/            # Shared Utilities
│   ├── database/             # Data Layer
│   │   ├── models.py         # SQLAlchemy ORM Models
│   │   └── session.py        # Database Connection
│   └── main.py               # API Entry Point
│
├── tests/                    # Test Suite
└── README.md                 # Project Documentation
```

## Setup

Follow these instructions to get Shiftly running locally.

### 1. Clone the repository

```bash
git clone https://github.com/your-username/shiftly.git
cd shiftly
```

### 2. Create a virtual environment (recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Install dependencies

```bash
pip install -r backend/requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the root of the project:

```bash
# Database Configuration
DB_HOST=your_database_host
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password

# JWT Authentication
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Set up the database

The application uses SQLite by default for development. The database tables will be created automatically when you run the application for the first time.

For production with PostgreSQL, update your `DATABASE_URL` in the `.env` file:

```bash
DATABASE_URL=postgresql://user:password@localhost/dbname
```

Then create the tables:

```bash
# If you have migration scripts
alembic upgrade head

# Or create tables programmatically
python -c "from backend.database.auth import Base; from backend.database.models import Base as ModelsBase; from backend.database.session import engine; Base.metadata.create_all(bind=engine); ModelsBase.metadata.create_all(bind=engine)"
```

### 6. Run the FastAPI server

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### 7. Access the API documentation

FastAPI provides interactive API documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### 8. Generate a schedule

Use the `/schedule/generate` endpoint with a POST request containing a start date:

```json
{
  "start_date": "2025-11-25"
}
```

The API will return:
- **assignments**: List of talent-to-shift assignments with details
- **understaffed**: List of shifts that couldn't be fully staffed