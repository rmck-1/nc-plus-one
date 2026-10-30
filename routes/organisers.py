from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from models.auth_models import get_current_user
# from models.organisers_models import 

router = APIRouter(prefix="/organisers", tags=["organisers stats"])

@router.get("/{organiser_id}/stats", status_code=200)
def get_organiser_stats(current_user_id: int = Depends(get_current_user)):
    pass