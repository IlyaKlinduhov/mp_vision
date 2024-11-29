from connection import *

async def get_all_users():
    query = '''
        SELECT user_id, token FROM users;
    '''

    conn = await get_db_connection()

    user_dict = {}
    try:
        user_dict = [dict(row) for row in await conn.fetch(query)]
    finally:
        await close_db_connection(conn)

    return user_dict