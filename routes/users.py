from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from models.auth_models import get_current_user
from models.users_models import user_events

router = APIRouter(prefix="/user/me/events", tags=["user events"])

@router.get("", status_code=200)
def get_user_events(current_user_id: int = Depends(get_current_user)):
    events = user_events(current_user_id)
    if events is False:
        raise HTTPException(status_code=500,
                                    detail={"code": "ERROR", 
                                            "message": "Database error occurred"})
    return {"events": events}