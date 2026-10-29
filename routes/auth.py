from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from schemas.auth_schema import LoginRequest, RegisterRequest
from models.auth_models import get_user, register_new_user
from utils.password_hash import verify_password
from utils.jwt_utils import create_access_token

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/login", status_code=200)
def login(body: LoginRequest):
    user = get_user(body.email)
    if not user or not verify_password(body.password, user['password']):
        raise HTTPException(
            status_code = 401,
            detail={"code": "UNAUTHORISED",
                    "message": "Incorrect email or password"},
            headers={"headers": "WWW-Authenticate"}
        )
    if verify_password(body.password, user['password']):
        return {"user_token":{
            "access_token": create_access_token(user["id"]),
            "token_type": "bearer"
        }}

@router.post("/register", status_code=201)
def register_user(body: RegisterRequest):
    new_user = register_new_user(body.name, body.email, body.password)
    if not new_user:
        raise HTTPException(
            status_code = 409,
            detail={"code": "EMAIL_IN_USE",
                    "message": "email address already registered"}
        )
    return {"user": new_user}
