from fastapi import FastAPI, APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
import os
import secrets
import asyncpg
from typing import Annotated
from datetime import timedelta, datetime, timezone
from app.auth.security import authenticate_user, user_in_db, verify_token_type, create_jwt, token_in_db, get_user, required_roles, store_token
from app.auth.models import Token, UserInDB, TokenPayload, UserInvite, AcceptInvite, InviteToken, sendRequest, createUser, UserRole
from app.database.database import get_db, asyncSQLRepo
from app.auth.utils import send_email, hash_password, generate_temporary_password

auth_router = APIRouter()

SECRET_KEY = os.getenv("KEY")
algorithm = "HS256"


@auth_router.post("/create", response_model=UserInvite)
async def create_user(user: Annotated[createUser, Body()],
                       db: Annotated[asyncpg.Connection, Depends(get_db)],
                        _: str = Depends(required_roles(UserRole.superuser, UserRole.admin))) -> UserInvite:
    username = f"{user.firstname.strip().lower()}.{user.lastname.strip().lower()}"
    user_exists = await user_in_db(db, username=username)
    if user_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User already exists")
    insert_query = "INSERT INTO users (username, firstname, lastname, email, user_role, pwd_hash, is_active) VALUES ($1, $2, $3, $4 ,$5 ,$6, $7) RETURNING id" 
    temporary = generate_temporary_password()
    hashed = hash_password(temporary)
    row = await db.fetchrow(insert_query, username, user.firstname, user.lastname, user.email, user.user_role, hashed, False) 
    id = row["id"]
    return UserInvite(sub=id,username=username, email=user.email, role=user.user_role, password=temporary) 

