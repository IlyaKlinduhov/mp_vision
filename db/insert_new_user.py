from connection import *

async def insert_new_user(login, token):
    query = '''
        INSERT INTO users (login, token) VALUES ($1, $2) RETURNING user_id;
    '''

    conn = await get_db_connection()

    user_id = None
    try:
        user_id = await conn.fetchval(query, login, token)
    finally:
        await close_db_connection(conn)

    if user_id is not None:
        return user_id