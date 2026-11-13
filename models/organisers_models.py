# from db.seed.connections import get_connection
# import psycopg2.extras
# from psycopg2.errors import ForeignKeyViolation

# def organiser_stats(user_id):
#     conn = get_connection()
#     cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
#     try:
#         cursor.execute("""
#         SELECT users.id AS organiser_id, users.name, 
#         COUNT(DISTINCT events.id) AS total_events,
#         COALESCE(
#             ROUND(COUNT(rsvps.event_id)::numeric / NULLIF(COUNT(DISTINCT events.id), 0), 2), 0)
#         AS avg_attendance
#         FROM users
#         LEFT JOIN events ON users.id = events.organiser_id
#         LEFT JOIN rsvps ON events.id = rsvps.event_id
#         WHERE users.id = %s
#         GROUP BY users.id, users.name;
#         """, (user_id,))
#         stats = cursor.fetchall()
#         return stats
#     except Exception:
#         conn.rollback()
#         return False
#     finally:
#         cursor.close()
#         conn.close()