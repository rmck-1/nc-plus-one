from connections import get_connection
import json

def drop_table_events(cursor):
    """Drops events table to start fresh when seed runs"""
    drop_events_table = """
    DROP TABLE IF EXISTS events;
    """
    cursor.execute(drop_events_table)

def create_table_events(cursor):
    """Creates events table fresh when seed runs"""
    create_events_table = """
    CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description VARCHAR(255),
    starts_at TIMESTAMPTZ NOT NULL,
    ends_at TIMESTAMPTZ NOT NULL,
    organiser_id INT REFERENCES users(id),
    venue_id INT REFERENCES venues(id),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
    );
    """
    cursor.execute(create_events_table)

def get_events():
    """I/O to get events.json file"""
    with open ("./db/data/events.json") as file:
        events = json.load(file)
    return events

def insert_events(cursor, events):
    """Loops through the events.json data and inserts each event into the event table"""
    events_list = events
    insert_users = """
     INSERT INTO events
     (title, description, starts_at, ends_at, organiser_id, venue_id)
     VALUES (%s, %s, %s, %s, %s, %s)
     """   
    for event in events_list:
        cursor.execute(insert_users, (event["title"], event["description"], event["starts_at"], event["ends_at"], event["organiser_id"], event["venue_id"]))

def seed_events():
    """Completes all events seeding by calling every function"""
    conn = get_connection()
    cursor = conn.cursor()
    drop_table_events(cursor)
    create_table_events(cursor)
    events = get_events()
    insert_events(cursor, events)
    conn.commit()
    cursor.close()
    conn.close()
