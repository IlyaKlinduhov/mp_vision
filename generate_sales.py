from connection import *
import random
from generate_stocks import warehouses
from generate_orders import get_last_30_days
from datetime import datetime, timedelta
import asyncio

async def insert_sales_for_one_user_for_one_day(user_id, date, conn):
    try:
        skus_rows = await conn.fetch('SELECT sku, nmid FROM skus WHERE nmid IN (SELECT nmid FROM nmids WHERE user_id = $1)', user_id)

        values = []
        for row in skus_rows:

            quantity = random.randint(1, 22)
            warehouse = random.choice(warehouses)
            sum_for_pay = random.randint(500, 5000)
            order_sum = random.randint(700, 7000)
            values.append((date, True, row[0], warehouse, quantity, sum_for_pay, order_sum, row[1]))

            if random.uniform(0, 1) > 0.85:
                values.append((
                    date, False, row[0], warehouse, random.randint(1, 4), 
                    random.randint(-1500, -500), random.randint(-1900, -700), row[1]
                ))


        
        sales_query = '''
                        INSERT INTO sales (date, flag, sku, warehouse, quantity, sum_for_pay, order_sum, nmid)
                        VALUES ($1, $2, $3, $4, $5, $6, $7, $8);
                    '''
        
        await conn.executemany(sales_query, values)

    finally:
        await close_db_connection(conn)



async def insert_sales_by_30_days_for_user(user_id):
    days = get_last_30_days()
    for day in days:
        conn = await get_db_connection()
        await insert_sales_for_one_user_for_one_day(user_id, day, conn)



async def insert_yesterday_sales_for_user(user_id):
    yesterday = datetime.now().date() - timedelta(days=1)
    conn =await get_db_connection_with_semaphore()
    await insert_sales_for_one_user_for_one_day(user_id, yesterday, conn)



async def delete_yesterday_sales(user_id):
    yesterday = datetime.now().date() - timedelta(days=1)

    conn = await get_db_connection_with_semaphore()
    try:
        await conn.execute(
            'DELETE FROM sales WHERE date = $1 AND nmid IN (SELECT nmid FROM nmids WHERE user_id = $2)',
            yesterday, user_id
            )
    finally:
        await close_db_connection(conn)



async def update_sales_for_user(user_id):
    await delete_yesterday_sales(user_id)
    await insert_yesterday_sales_for_user(user_id)
    

async def delete_depricated_rows_in_sales():
    today = datetime.now().date()
    depricated_day = today - timedelta(days=31)

    conn = await get_db_connection()
    try:
        await conn.execute('DELETE FROM sales WHERE date <= $1', depricated_day)
    finally:
        await close_db_connection(conn)

if __name__ == '__main__':
    asyncio.run(insert_sales_by_30_days_for_user(30))
