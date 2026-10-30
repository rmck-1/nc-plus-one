from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from typing import Optional
from schemas.events_schema import EventsResponse, EventResponse, CreateEvent, ReturnEventResponse, PatchEvent
from models.events_models import get_events_venue_id_query_parameter, get_events_organiser_id_query_parameter, get_all_events, get_event_id, create_new_event, update_event, event_attendees
from models.auth_models import get_current_user
from models.rsvp_models import has_user_rsvpd, rsvp_for_event, delete_user_rsvp

router = APIRouter(prefix="/events", tags=["events"])


@router.get("", status_code=200, response_model=EventsResponse)
def get_events(venue_id: Optional[int]=None, organiser_id: Optional[int]=None):
    """get events endpoint that returns a dictionary with a list of
     events as the key ordered by the start date in ascending order.
     Accepts query parameters for venue_id and organiser_id"""
    if venue_id:
        rows = get_events_venue_id_query_parameter(venue_id)
    elif organiser_id:
        rows = get_events_organiser_id_query_parameter(organiser_id)
    else:
        rows = get_all_events()
    return {"events": rows}

@router.get("/{event_id}", status_code=200, response_model=EventResponse)
def get_event(event_id: int):
    """get event endpoint that returns a dictionary with the specified event and
    the venue name from a join table. It has error handling for 404 and 400 status codes"""
    row = get_event_id(event_id)
    if row is None:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", 
                                                     "message": "Event not found"})
    return {"event": row}

@router.post("/{event_id}/rsvp", status_code=201)
def event_rsvp(event_id: int, current_user_id: int = Depends(get_current_user)):
    check_event_exists = get_event_id(event_id)
    if check_event_exists is None:
            raise HTTPException(status_code=404,
                                detail={"code": "NOT_FOUND",
                                        "message": "Event not found"})
    check_user_registered = has_user_rsvpd(current_user_id, event_id)
    if check_user_registered:
         raise HTTPException(status_code=409,
                             detail={"code": "CONFLICT", 
                                    "message": "Already registered for event"})
    new_rsvp = rsvp_for_event(current_user_id, event_id)
    return {"rsvp": new_rsvp}

@router.delete("/{event_id}/rsvp/me", status_code=204)
def delete_rsvp(event_id: int, current_user_id: int = Depends(get_current_user)):
    success = delete_user_rsvp(current_user_id, event_id)
    if not success:
        raise HTTPException(status_code=404,
                            detail={"code": "NOT_FOUND", 
                                    "message": "Not registered for event"})
    return

@router.post("", status_code=201, response_model=ReturnEventResponse)
def post_event(event: CreateEvent, current_user_id: int = Depends(get_current_user)):
    event_details = create_new_event(current_user_id, event.title, event.description, event.starts_at, event.ends_at, event.venue_id)
    if event_details == "VENUE_NOT_FOUND":
        raise HTTPException(status_code=404,
                            detail={"code": "NOT_FOUND", 
                                    "message": "Venue not found"})
    return {"event": event_details}

@router.patch("/{event_id}", status_code=200)
def patch_event(event_id: int, event: PatchEvent, current_user_id: int = Depends(get_current_user)):
    existing_event = get_event_id(event_id)
    if existing_event is None:
        raise HTTPException(status_code=404,
                            detail={"code": "NOT_FOUND", 
                                    "message": "Event not found"})    
    if current_user_id != existing_event["organiser_id"]:
        raise HTTPException(status_code=403,
                            detail={"code": "FORBIDDEN", 
                                    "message": "User is not the event owner"})
    # below code is to catch only one date being provided that would make the starts_at greater than end date, if both are provided this is handled in the PatchEvent BaseModel
    final_starts_at = event.starts_at if event.starts_at else existing_event["starts_at"]
    final_ends_at = event.ends_at if event.ends_at else existing_event["ends_at"]
    if final_starts_at >= final_ends_at:
        raise HTTPException(status_code=400,
                            detail={"code": "INVALID_INPUT", 
                                    "message": "start_at must be before ends_at"})
    update_dict = event.model_dump(exclude_unset=True)
    updated_event = update_event(event_id, update_dict)
    if updated_event is None:
        return {"event": existing_event}
    return {"event": updated_event}

@router.get("/{event_id}/attendees", status_code=200)
def get_event_attendees(event_id: int, current_user_id: int = Depends(get_current_user)):
    existing_event = get_event_id(event_id)
    if existing_event is None:
        raise HTTPException(status_code=404,
                            detail={"code": "NOT_FOUND", 
                                    "message": "Event not found"})    
    if current_user_id != existing_event["organiser_id"]:
        raise HTTPException(status_code=403,
                            detail={"code": "FORBIDDEN", 
                                    "message": "User is not the event owner"})
    attendees = event_attendees(event_id)
    if attendees is False:
        raise HTTPException(status_code=500,
                            detail={"code": "ERROR", 
                                    "message": "Database error occurred"})  
    return {"attendees": attendees}