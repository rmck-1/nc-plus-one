def get_all_events(cursor):
    cursor.execute("""
    SELECT events.id, events.title, events.description, events.starts_at, events.ends_at, events.organiser_id, events.venue_id,
    venues.name AS venue_name, venues.address AS venue_address, venues.capacity AS venue_capacity
    FROM events
    INNER JOIN venues ON events.venue_id = venues.id
    ORDER BY starts_at ASC;
    """)
    return cursor

def get_events_venue_id_query_parameter(venue_id, cursor):
    cursor.execute("""
    SELECT events.id, events.title, events.description, events.starts_at, events.ends_at, events.organiser_id, events.venue_id,
    venues.name AS venue_name, venues.address AS venue_address, venues.capacity AS venue_capacity
    FROM events
    INNER JOIN venues ON events.venue_id = venues.id
    WHERE venue_id = %s
    ORDER BY starts_at ASC;
    """, (venue_id,))
    return cursor

def get_events_organiser_id_query_parameter(organiser_id, cursor):
    cursor.execute("""
    SELECT events.id, events.title, events.description, events.starts_at, events.ends_at, events.organiser_id, events.venue_id,
    venues.name AS venue_name, venues.address AS venue_address, venues.capacity AS venue_capacity
    FROM events
    INNER JOIN venues ON events.venue_id = venues.id
    WHERE organiser_id = %s
    ORDER BY starts_at ASC;
    """, (organiser_id,))
    return cursor

def get_event_id(event_id, cursor):
    cursor.execute("""
    SELECT events.id, events.title, events.description, events.starts_at, events.ends_at, events.organiser_id, events.venue_id, events.created_at,
    venues.name AS venue_name, venues.address AS venue_address, venues.capacity AS venue_capacity
    FROM events
    INNER JOIN venues ON events.venue_id = venues.id
    WHERE events.id = %s;
    """, (event_id,))
    return cursor