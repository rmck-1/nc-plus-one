from fastapi import APIRouter, HTTPException
import psycopg2.extras
from db.seed.connections import get_connection

router = APIRouter(prefix="/events", tags=["events"])

@router.get("", status_code=200)
def get_events():
    """get events endpoint that returns a dictionary with a list of
     events as the key ordered by the start date in ascending order"""
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
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
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM events
    WHERE id = %s;
    """, (event_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return {"event": [{"id": row[0],
                      "title": row[1],
                      "description": row[2],
                      "starts_at": row[3],
                      "ends_at": row[4],
                      "organiser_id": row[5],
                      "venue_id": row[6]}]}