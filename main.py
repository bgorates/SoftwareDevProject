from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from backend.core.talents.routes import talents
from backend.core.schedule.routes import schedule
from backend.core.constraints.talent_constraints.routes import talent_constraints
from backend.core.constraints.constraint_rules.routes import constraint_rules
from backend.core.shift_template.routes import shift_templates
from backend.core.shift_period.routes import shift_period
from backend.authentication.routes import auth_router


app = FastAPI(title="Shiftly", version="1.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth_router, prefix="/users")
app.include_router(talents, prefix="/talents")
app.include_router(talent_constraints, prefix="/talent_constraints")
app.include_router(constraint_rules, prefix="/constraint_rules")
app.include_router(shift_period, prefix="/shift_period")
app.include_router(shift_templates, prefix="/shift_templates")
app.include_router(schedule, prefix="/schedule")

# Mount static files (CSS, JS, images, etc.)
frontend_path = Path(__file__).parent / "frontend"
app.mount("/css", StaticFiles(directory=str(frontend_path / "css")), name="css")
app.mount("/js", StaticFiles(directory=str(frontend_path / "js")), name="js")
app.mount("/components", StaticFiles(directory=str(frontend_path / "components")), name="components")

# Mount pages directory for static assets (CSS, JS files within pages)
app.mount("/pages", StaticFiles(directory=str(frontend_path / "pages")), name="pages")

# Serve frontend pages (HTML files)
@app.get("/")
async def read_root():
    """Serve the main index.html page"""
    return FileResponse(str(frontend_path / "index.html"))

# Serve favicon
@app.get("/favicon.ico")
async def favicon():
    """Serve the favicon"""
    favicon_path = frontend_path / "favicon.ico"
    if favicon_path.exists():
        return FileResponse(str(favicon_path))
    return {"error": "Favicon not found"}, 404









