from fastapi import APIRouter
from fastapi.exceptions import HTTPException
import psycopg2.extras
from db.seed.connections import get_connection
from typing import Optional

router = APIRouter(prefix="/events", tags=["events"])

@router.get("", status_code=200)
def get_events(venue_id: Optional[int]=None, organiser_id: Optional[int]=None):
    """get events endpoint that returns a dictionary with a list of
     events as the key ordered by the start date in ascending order"""
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    if venue_id:
        cursor.execute("""
        SELECT * FROM events
        WHERE venue_id = %s
        ORDER BY starts_at ASC;
        """, (venue_id,))
    elif organiser_id:
        cursor.execute("""
        SELECT * FROM events
        WHERE organiser_id = %s
        ORDER BY starts_at ASC;
        """, (organiser_id,))
    else:
        cursor.execute("""
        SELECT * FROM events
        ORDER BY starts_at ASC;
        """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return {"events": rows}

@router.get("/{event_id}", status_code=200)
def get_event(event_id: int):
    """get event endpoint that returns a dictionary with the specified event and
    the venue name from a join table. It has error handling for 404 and 400 status codes"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT events.id, events.title, events.description, events.starts_at, events.ends_at, events.organiser_id, events.venue_id,
    venues.name
    FROM events
    INNER JOIN venues ON events.venue_id = venues.id
    WHERE events.id = %s;
    """, (event_id,))
    row = cursor.fetchone()
    if row is None:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", 
                                                     "message": "Event not found"})
    cursor.close()
    conn.close()
    return {"event": [{"id": row[0],
                      "title": row[1],
                      "description": row[2],
                      "starts_at": row[3],
                      "ends_at": row[4],
                      "organiser_id": row[5],
                      "venue_id": row[6],
                      "venue": row[7]}]}