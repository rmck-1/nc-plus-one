from connections import get_connection
import json
 
def drop_table_users(cursor):
    """Drops users table to start fresh when seed runs"""
    drop_users_table = """
    DROP TABLE IF EXISTS users;
    """
    cursor.execute(drop_users_table)

def create_table_users(cursor):
    """Creates user table fresh when seed runs"""
    create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    cursor.execute(create_users_table)

def get_users():
    """I/O to get users.json file"""
    with open ("./db/data/users.json") as file:
        users = json.load(file)
    return users


def insert_users(cursor, users):
    """Loops through the users.json data and inserts each user into the users table"""
    user_list = users
    insert_users = """
     INSERT INTO users
     (email, password, name)
     VALUES (%s, %s, %s)
     """   
    for user in user_list:
        cursor.execute(insert_users, (user["email"], user["password"], user["name"]))


def seed_users():
    """Completes all user seeding by calling every function"""
    conn = get_connection()
    cursor = conn.cursor()
    drop_table_users(cursor)
    create_table_users(cursor)
    users = get_users()
    insert_users(cursor, users)
    conn.commit()
    cursor.close()
    conn.close()
