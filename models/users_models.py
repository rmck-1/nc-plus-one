from db.seed.connections import get_connection
import psycopg2.extras
from psycopg2.errors import ForeignKeyViolation

def user_events(user_id):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        cursor.execute("""
        SELECT rsvps.event_id, events.title, events.starts_at, 
        rsvps.created_at AS rsvp_date,
        (SELECT COUNT(*) FROM rsvps AS r2 WHERE r2.event_id = events.id) as total_rsvps,
        RANK() OVER (ORDER BY events.starts_at ASC) AS event_rank
        FROM rsvps
        INNER JOIN events ON rsvps.event_id = events.id
        WHERE rsvps.attendee_id = %s;
        """, (user_id,))
        events = cursor.fetchall()
        return events
    except Exception:
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()
