from db.seed.users_seed import seed_users, drop_table_users
from db.seed.venues_seed import seed_venues, drop_table_venues
from db.seed.events_seed import seed_events, drop_table_events
from db.seed.rsvps_seed import seed_rsvps, drop_table_rsvps
from db.seed.connections import get_connection

# seeds the database tables
# python -m db.seed.seed - to seed normal DB
# ENV=test -m db.seed.seed - to seed test DB

def drop_tables():
    conn = get_connection()
    cursor = conn.cursor()
    drop_table_rsvps(cursor)
    drop_table_events(cursor)
    drop_table_venues(cursor)
    drop_table_users(cursor)
    conn.commit()
    cursor.close()
    conn.close()

def drop_and_seed_tables():
    drop_tables()
    seed_users()
    seed_venues()
    seed_events()
    seed_rsvps()

drop_and_seed_tables()





