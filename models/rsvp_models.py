from db.seed.connections import get_connection
from psycopg2.errors import ForeignKeyViolation
import psycopg2.extras

def has_user_rsvpd(user_id: int, event_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT EXISTS (
    SELECT 1
    FROM rsvps
    WHERE attendee_id = %s AND event_id = %s
    );
    """, (user_id, event_id))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0]

def rsvp_for_event(user_id: int, event_id: int):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("""
    INSERT INTO rsvps
    (attendee_id, event_id)
    VALUES (%s, %s)
    RETURNING id, attendee_id, event_id, created_at;
    """, (user_id, event_id))
    new_rsvp = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    return new_rsvp

def delete_user_rsvp(user_id: int, event_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        DELETE FROM rsvps
        WHERE attendee_id = %s
        AND event_id = %s;
        """, (user_id, event_id))
        if cursor.rowcount != 1:
            conn.rollback()
            return False
        conn.commit()
        return True
    except Exception:
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()