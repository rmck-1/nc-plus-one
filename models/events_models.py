from db.seed.connections import get_connection
import psycopg2.extras
from psycopg2.errors import ForeignKeyViolation

def get_all_events():
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("""
    SELECT events.id, events.title, events.description, events.starts_at, events.ends_at, events.organiser_id, events.venue_id,
    venues.name AS venue_name, venues.address AS venue_address, venues.capacity AS venue_capacity
    FROM events
    INNER JOIN venues ON events.venue_id = venues.id
    ORDER BY starts_at ASC;
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def get_events_venue_id_query_parameter(venue_id):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)    
    cursor.execute("""
    SELECT events.id, events.title, events.description, events.starts_at, events.ends_at, events.organiser_id, events.venue_id,
    venues.name AS venue_name, venues.address AS venue_address, venues.capacity AS venue_capacity
    FROM events
    INNER JOIN venues ON events.venue_id = venues.id
    WHERE venue_id = %s
    ORDER BY starts_at ASC;
    """, (venue_id,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def get_events_organiser_id_query_parameter(organiser_id):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)     
    cursor.execute("""
    SELECT events.id, events.title, events.description, events.starts_at, events.ends_at, events.organiser_id, events.venue_id,
    venues.name AS venue_name, venues.address AS venue_address, venues.capacity AS venue_capacity
    FROM events
    INNER JOIN venues ON events.venue_id = venues.id
    WHERE organiser_id = %s
    ORDER BY starts_at ASC;
    """, (organiser_id,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def get_event_id(event_id):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("""
    SELECT events.id, events.title, events.description, events.starts_at, events.ends_at, events.organiser_id, events.venue_id, events.created_at,
    venues.name AS venue_name, venues.address AS venue_address, venues.capacity AS venue_capacity
    FROM events
    INNER JOIN venues ON events.venue_id = venues.id
    WHERE events.id = %s;
    """, (event_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row

def create_new_event(user_id, title, description, starts_at, ends_at, venue_id):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)    
    try:
        cursor.execute("""
        INSERT INTO events
        (title, description, starts_at, ends_at, organiser_id, venue_id)
        VALUES
        (%s, %s, %s, %s, %s, %s)
        RETURNING id, title, description, starts_at, ends_at, venue_id, organiser_id, created_at;
        """, (title, description, starts_at, ends_at, user_id, venue_id))
        new_event = cursor.fetchone()
        conn.commit()
        return new_event
    except ForeignKeyViolation:
        conn.rollback()
        return "VENUE_NOT_FOUND"
    except Exception:
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

def update_event(event_id: int, update_fields: dict):
    """
    Update an existing event in the events table.
    What fields that are passed to the function can vary (description, starts_at, ends_at)
    Meaning the SQL statement also has to vary and be constructed dynamically

    Args:
        fields from the events_schema PatchEvent Class
    Returns:
        the newly updated row from the events table
    """
    if not update_fields: # checks that the request body has passed in fields to update
        return None
    conditions = [] # the columns to update in the SET statement
    values = [] # the values to pass in
    for column, value in update_fields.items(): # this populates the two lists
        conditions.append(f"{column} = %s") 
        values.append(value)
    query_string = ", ".join(conditions) # this creates the full query string
    values.append(event_id) # added to the end of the list because this is the condition for the WHERE clause
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        query = f"""
        UPDATE events
        SET {query_string}
        WHERE id = %s
        RETURNING *;
        """
        cursor.execute(query, tuple(values))
        updated_event = cursor.fetchone()
        conn.commit()
        return updated_event
    except Exception:
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()
