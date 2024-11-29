from connection import * 
import random
from generate_orders import get_last_30_days
from datetime import datetime, timedelta
import asyncio

async def insert_salesfunel_for_one_user_for_one_day(user_id, date, conn):
    try:
        skus_rows = await conn.fetch('SELECT nmid FROM nmids WHERE user_id = $1', user_id)

        values = []
        for row in skus_rows:

            open_card_count = random.randint(20, 2000)
            add_to_cart_count = random.randint(1, open_card_count // 8)
            values.append((date, row[0], open_card_count, add_to_cart_count, (add_to_cart_count / open_card_count) * 100))
        
        salesfunel_query = '''
                        INSERT INTO salesfunel (date, nmid, open_card_count, add_to_cart_count, add_to_cart_percent)
                        VALUES ($1, $2, $3, $4, $5);
                    '''
        
        await conn.executemany(salesfunel_query, values)

    finally:
        await close_db_connection(conn)



async def insert_salesfunel_by_30_days_for_user(user_id):
    days = get_last_30_days()
    for day in days:
        conn = await get_db_connection()
        await insert_salesfunel_for_one_user_for_one_day(user_id, day, conn)



async def insert_yesterday_salesfunel_for_user(user_id):
    yesterday = datetime.now().date() - timedelta(days=1)
    conn =await get_db_connection_with_semaphore()
    await insert_salesfunel_for_one_user_for_one_day(user_id, yesterday, conn)



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



async def update_salesfunel_for_user(user_id):
    await delete_yesterday_salesfunel(user_id)
    await insert_yesterday_salesfunel_for_user(user_id)


async def delete_depricated_rows_in_salesfunel():
    today = datetime.now().date()
    depricated_day = today - timedelta(days=31)

    conn = await get_db_connection()
    try:
        await conn.execute('DELETE FROM salesfunel WHERE date <= $1', depricated_day)
    finally:
        await close_db_connection(conn)



if __name__ == '__main__':
    asyncio.run(insert_salesfunel_by_30_days_for_user(30))