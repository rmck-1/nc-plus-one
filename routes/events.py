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