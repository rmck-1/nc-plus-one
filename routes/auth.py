from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from db.seed.connections import get_connection
from schemas.auth_schema import LoginRequest
from models.auth_models import get_user
from utils.password_hash import verify_password
from utils.jwt_utils import create_access_token

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/login")
def login(body: LoginRequest):
    user = get_user(body.email)
    if verify_password(body.password, user["user"]['password']):
        return {"user token:":{
            "access_token": create_access_token(user["user"]["id"]),
            "token_type": "bearer"
        }}
    return "not found"