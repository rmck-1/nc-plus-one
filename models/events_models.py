from db.seed.connections import get_connection
import psycopg2.extras

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