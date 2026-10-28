from fastapi import APIRouter
from fastapi.exceptions import HTTPException
import psycopg2.extras
from db.seed.connections import get_connection
from typing import Optional
from schemas.events_schema import EventsResponse, EventResponse
from models.events_models import get_events_venue_id_query_parameter, get_events_organiser_id_query_parameter, get_all_events, get_event_id

router = APIRouter(prefix="/events", tags=["events"])

@router.get("", status_code=200, response_model=EventsResponse)
def get_events(venue_id: Optional[int]=None, organiser_id: Optional[int]=None):
    """get events endpoint that returns a dictionary with a list of
     events as the key ordered by the start date in ascending order.
     Accepts query parameters for venue_id and organiser_id"""
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    if venue_id:
        get_events_venue_id_query_parameter(venue_id, cursor)
    elif organiser_id:
        get_events_organiser_id_query_parameter(organiser_id, cursor)
    else:
        get_all_events(cursor)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return {"events": rows}

@router.get("/{event_id}", status_code=200, response_model=EventResponse)
def get_event(event_id: int):
    """get event endpoint that returns a dictionary with the specified event and
    the venue name from a join table. It has error handling for 404 and 400 status codes"""
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    get_event_id(event_id, cursor)
    row = cursor.fetchone()
    if row is None:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", 
                                                     "message": "Event not found"})
    cursor.close()
    conn.close()
    return {"event": row}