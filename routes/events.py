from fastapi import APIRouter, HTTPException
from db.seed.connections import get_connection

router = APIRouter(prefix="/events", tags=["events"])