from connection import *
from datetime import datetime, timedelta

async def save_adverts_to_db(advert_map):
    conn = await get_db_connection()
    try:
        async with conn.transaction():
            if len(advert_map) > 0:
                for advert in advert_map:
                    if len(advert_map) != 0:
                        stat = advert_map.get(advert)

                        nmid = await conn.fetchval('SELECT nmid FROM nmids WHERE nmid = $1', str(stat['nmid']))

                        if nmid is None:
                            continue

                        query = '''
                            INSERT INTO advert (date, advertid, nmid, views, clicks, sum, is_auto) 
                            VALUES ($1, $2, $3, $4, $5, $6, $7)
                            ON CONFLICT DO NOTHING 
                        '''

                        if stat['type'] == 8:
                            is_auto = True
                        else:
                            is_auto = False

                        await conn.execute(
                            query, stat['date'], str(stat['advertId']), str(stat['nmid']), stat['views'],
                            stat['clicks'], stat['sum'], is_auto
                        )
    finally:
        await close_db_connection(conn)



async def delete_yesterday_adverts(user_id):
    yesterday = datetime.now().date() - timedelta(days=1)

    conn = await get_db_connection_with_semaphore()
    try:
        await conn.execute(
            'DELETE FROM advert WHERE date = $1 AND nmid IN (SELECT nmid FROM nmids WHERE user_id = $2)',
            yesterday, user_id
            )
    finally:
        await close_db_connection(conn)


async def delete_depricated_rows_in_adverts():
    today = datetime.now().date()
    depricated_day = today - timedelta(days=31)

    conn = await get_db_connection()
    try:
        await conn.execute('DELETE FROM advert WHERE date <= $1', depricated_day)
    finally:
        await close_db_connection(conn)