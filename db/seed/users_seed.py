from connections import get_connection
import json
# Drops users table to start fresh when seed runs
def drop_table_users(cursor):
    drop_users_table = """
    DROP TABLE users;
    """
    cursor.execute(drop_users_table)

# Creates user table fresh when seed runs
def create_table_users(cursor):
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

# I/O to get users.json file
def get_users():
    with open ("./db/data/users.json") as file:
        users = json.load(file)
    return users

# Loops through the users.json data and inserts each user into the users table
def insert_users(cursor, users):
    user_list = users
    insert_users = """
     INSERT INTO users
     (email, password, name)
     VALUES (%s, %s, %s)
     """   
    for user in user_list:
        cursor.execute(insert_users, (user["email"], user["password"], user["name"]))

# Completes all user seeding by calling every function
def seed_users():
    conn = get_connection()
    cursor = conn.cursor()
    drop_table_users(cursor)
    create_table_users(cursor)
    users = get_users()
    insert_users(cursor, users)
    conn.commit()
    cursor.close()
    conn.close()
