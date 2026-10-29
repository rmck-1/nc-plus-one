from db.seed.connections import get_connection
from utils.password_hash import hash_password
from psycopg2.errors import UniqueViolation
import psycopg2.extras

def get_user(email):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    user = cursor.execute("""
    SELECT * FROM users
    WHERE email = %s
    """, (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def register_new_user(name, email, password):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        cursor.execute("""
        INSERT INTO users
        (name, email, password)
        VALUES (%s, %s, %s)
        RETURNING id, name, email, created_at;
        """, (name, email, hash_password(password)))
        new_user = cursor.fetchone()
        conn.commit()
        return new_user
    except UniqueViolation:
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()