from connection import *
from datetime import datetime, timedelta

async def save_salesfunel_to_db(salesfunel_map):
    conn = await get_db_connection()
    try:
        async with conn.transaction():
            for salesfunel in salesfunel_map:
                stat = salesfunel_map.get(salesfunel)

                nmid = await conn.fetchval('SELECT nmid FROM nmids WHERE nmid = $1', str(stat['nmID']))

                if nmid is None:
                    continue

                query = '''
                    INSERT INTO salesfunel (date, nmid, open_card_count, add_to_cart_count, add_to_cart_percent) 
                    VALUES ($1, $2, $3, $4, $5)
                    ON CONFLICT DO NOTHING 
                '''

                await conn.execute(
                    query, stat['date'], str(stat['nmID']), stat['openCardCount'],
                    stat['addToCartCount'], stat['addToCartPercent']
                )
    finally:
        await close_db_connection(conn)


async def delete_yesterday_salesfunel(user_id):
    yesterday = datetime.now().date() - timedelta(days=1)

    conn = await get_db_connection_with_semaphore()
    try:
        await conn.execute(
            'DELETE FROM salesfunel WHERE date = $1 AND nmid IN (SELECT nmid FROM nmids WHERE user_id = $2)',
            yesterday, user_id
        )
    finally:
        await close_db_connection(conn)


async def delete_depricated_rows_in_salesfunel():
    today = datetime.now().date()
    depricated_day = today - timedelta(days=31)

    conn = await get_db_connection()
    try:
        await conn.execute('DELETE FROM salesfunel WHERE date <= $1', depricated_day)
    finally:
        await close_db_connection(conn)