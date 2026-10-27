from users_seed import seed_users, drop_table_users
from venues_seed import seed_venues, drop_table_venues
from events_seed import seed_events, drop_table_events
from rsvps_seed import seed_rsvps, drop_table_rsvps
from connections import get_connection

# seed the user, venues table in the database.

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






