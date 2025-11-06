from fastapi import FastAPI
from app.auth.routes import auth_router
import secrets


app = FastAPI(title="Employee Shift Management", version=1.0)
app.include_router(auth_router, prefix="/users")
