from db.seed.connections import get_connection
from utils.password_hash import hash_password
from psycopg2.errors import UniqueViolation
import psycopg2.extras
from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from utils.jwt_utils import get_secret, ALGORITHM
import jwt

bearer_scheme = HTTPBearer(auto_error=False)

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

def get_current_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme)):
    unauthorised = HTTPException(status_code=401,
                                 detail={"code": "NOT_AUTHORISED",
                                         "message": "Token not valid"})
    if credentials is None:
        raise unauthorised
    try:
        payload = jwt.decode(credentials.credentials, get_secret(), ALGORITHM)
        customer_id = int(payload["sub"])
    except(jwt.InvalidTokenError, KeyError, ValueError):
        raise unauthorised
    return customer_id