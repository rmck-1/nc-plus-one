from db.seed.connections import get_connection
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
    return {"user": user}