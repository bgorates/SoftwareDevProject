from fastapi import APIRouter, Depends, Body, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated
from backend.authentication.users.schema import CreateUser, InviteTarget, NewPassword, UserOut
from backend.authentication.tokens.schema import TokenIn, TokenOut
from backend.database.session import session
from backend.database.auth import User
from backend.authentication.users.service import UserService
from backend.authentication.utils.auth_utils import get_current_user

auth_router = APIRouter(tags=['Users'])

@auth_router.post("/create")
def create_user(user: Annotated[CreateUser, Body()],
                db: Annotated[Session, Depends(session)]):
    return UserService.create_user(db=db, user=user)


@auth_router.post("/send_invite")
def invite_user(user_id:Annotated[InviteTarget, Body()], 
                      db: Annotated[Session, Depends(session)]
                      ):
    return UserService.invite_user(db=db, id=user_id)


@auth_router.post("/set_new_password")
def accept_invite(data: Annotated[NewPassword, Body ()], 
                        db: Annotated[Session, Depends(session)]):
    return UserService.set_new_password(data=data, db=db)

@auth_router.post("/login_token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                  db: Annotated[Session, Depends(session)]):
    login = UserService.login(form_data=form_data, db=db)
    return login

@auth_router.get("/list", response_model=list[UserOut])
def list_users(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(session)],
    role: str | None = Query(None, description="Filter users by role (e.g., 'manager', 'user', 'superuser')")
):
    """
    List all users, optionally filtered by role.
    
    Requires authentication. Only superusers should typically access this endpoint.
    
    Args:
        current_user: Authenticated user making the request.
        db: Database session.
        role: Optional role filter.
        
    Returns:
        List of UserOut objects.
    """
    return UserService.list_users(db=db, role=role)
  
  
 