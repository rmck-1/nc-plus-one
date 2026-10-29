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
    return "not found"