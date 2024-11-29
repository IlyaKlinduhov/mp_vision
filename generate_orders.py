from connection import *
from generate_stocks import warehouses
import random
from datetime import datetime, timedelta
import asyncio

def get_last_30_days():
    today = datetime.now().date()

    last_30_days = [(today - timedelta(days=i)) for i in range(1, 41)]
    return last_30_days



async def insert_orders_for_one_user_for_one_day(user_id, date, conn):
    try:
        skus_rows = await conn.fetch('SELECT sku, nmid FROM skus WHERE nmid IN (SELECT nmid FROM nmids WHERE user_id = $1)', user_id)

        values = []
        for row in skus_rows:
            quantity = random.randint(2, 25)
            warehouse = random.choice(warehouses)
            sum = random.randint(500, 5000)
            values.append((date, quantity, warehouse, row[1], sum, row[0]))
        
        orders_query = '''
                        INSERT INTO orders (date, quantity, warehouse, nmid, sum, sku)
                        VALUES ($1, $2, $3, $4, $5, $6);
                    '''
        
        await conn.executemany(orders_query, values)

    finally:
        await close_db_connection(conn)



async def insert_orders_by_30_days_for_user(user_id):
    days = get_last_30_days()
    for day in days:
        conn = await get_db_connection()
        await insert_orders_for_one_user_for_one_day(user_id, day, conn)



async def insert_yesterday_orders_for_user(user_id):
    yesterday = datetime.now().date() - timedelta(days=1)
    conn = await get_db_connection_with_semaphore()
    await insert_orders_for_one_user_for_one_day(user_id, yesterday, conn)



async def delete_yesterday_orders(user_id):
    yesterday = datetime.now().date() - timedelta(days=1)

    conn = await get_db_connection_with_semaphore()
    try:
        await conn.execute(
            'DELETE FROM orders WHERE date = $1 AND nmid IN (SELECT nmid FROM nmids WHERE user_id = $2)',
            yesterday, user_id
            )
    finally:
        await close_db_connection(conn)



async def delete_depricated_rows_in_orders():
    today = datetime.now().date()
    depricated_day = today - timedelta(days=31)

    conn = await get_db_connection()
    try:
        await conn.execute('DELETE FROM orders WHERE date <= $1', depricated_day)
    finally:
        await close_db_connection(conn)



async def update_orders_for_user(user_id):
    await delete_yesterday_orders(user_id)
    await insert_yesterday_orders_for_user(user_id)



if __name__ == '__main__':
    asyncio.run(insert_yesterday_orders_for_user(30))

