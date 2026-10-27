from db.seed.connections import get_connection
import json
import os

def drop_table_rsvps(cursor):
    """Drops rsvps table to start fresh when seed runs"""
    drop_rsvps_table = """
    DROP TABLE IF EXISTS rsvps;
    """
    cursor.execute(drop_rsvps_table)

def create_table_rsvps(cursor):
    """Creates rsvps table fresh when seed runs"""
    create_rsvps_table = """
    CREATE TABLE IF NOT EXISTS rsvps (
    id SERIAL PRIMARY KEY,
    attendee_id INT REFERENCES users(id),
    event_id INT REFERENCES events(id),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
    );
    """
    cursor.execute(create_rsvps_table)

def get_rsvps():
    """I/O to get rsvps.json file"""
    env = os.getenv("ENV", "development")
    folder = "test_data" if env == 'test' else "data"
    with open (f"./db/{folder}/rsvps.json") as file:
        rsvps = json.load(file)
    return rsvps

def insert_rsvps(cursor, rsvps):
    """Loops through the rsvps.json data and inserts each rsvp into the rsvps table"""
    rsvps_list = rsvps
    insert_rsvps = """
     INSERT INTO rsvps
     (attendee_id, event_id)
     VALUES (%s, %s)
     """   
    for rsvp in rsvps_list:
        cursor.execute(insert_rsvps, (rsvp["attendee_id"], rsvp["event_id"]))

def seed_rsvps():
    """Completes all rsvps seeding by calling every function"""
    conn = get_connection()
    cursor = conn.cursor()
    create_table_rsvps(cursor)
    events = get_rsvps()
    insert_rsvps(cursor, events)
    conn.commit()
    cursor.close()
    conn.close()