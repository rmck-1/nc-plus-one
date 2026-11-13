from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])

@router.get("", status_code=200)
def get_health():
    """get health endpoint that returns a 200 status code 
    if the API is active without querying the database"""
