from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from db.seed.connections import get_connection

router = APIRouter(prefix="/auth", tags=["authentication"])