from connections import get_connection
import json

def drop_table_venues(cursor):
    """Drops venues table to start fresh when seed runs"""
    drop_venues_table = """
    DROP TABLE IF EXISTS venues;
    """
    cursor.execute(drop_venues_table)

def create_table_venues(cursor):
    """Creates venues table fresh when seed runs"""
    create_venues_table = """
    CREATE TABLE IF NOT EXISTS venues (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address TEXT,
    capacity INT
    );
    """
    cursor.execute(create_venues_table)

def get_venues():
    """I/O to get venues.json file"""
    with open ("./db/data/venues.json") as file:
        venues = json.load(file)
    return venues

def insert_venues(cursor, venues):
    """Loops through the venues.json data and inserts each venue into the venue table"""
    venues_list = venues
    insert_users = """
     INSERT INTO venues
     (name, address, capacity)
     VALUES (%s, %s, %s)
     """   
    for venue in venues_list:
        cursor.execute(insert_users, (venue["name"], venue["address"], venue["capacity"]))

def seed_venues():
    """Completes all venue seeding by calling every function"""
    conn = get_connection()
    cursor = conn.cursor()
    create_table_venues(cursor)
    venues = get_venues()
    insert_venues(cursor, venues)
    conn.commit()
    cursor.close()
    conn.close()