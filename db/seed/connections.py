import os
import psycopg2
from dotenv import load_dotenv

# Establishes the connection to the database
def get_connection():
    env = os.getenv("ENV", "development")
    env_file = ".env.test" if env == "test" else ".env"
    load_dotenv(env_file, override=True)
    if not os.getenv("PGDATABASE"):
        raise RuntimeError("PGDATABASE NOT SET")
    connection = psycopg2.connect()
    return connection

## Uncomment below code and run file to verify the database connection is established ##
#conn = get_connection()
#print("Success! Connected to:", conn.info.dbname)