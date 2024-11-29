from connection import *
from datetime import datetime, timedelta

async def save_orders_to_db(orders):
    conn = await get_db_connection()
    try:
        async with conn.transaction():
            for order in orders:
                stat = orders.get(order)

                nmid = await conn.fetchval('SELECT nmid FROM skus WHERE sku = $1', str(stat['barcode']))

                if nmid is None:
                    continue

                query = '''
                    INSERT INTO orders (date, sku, warehouse, nmid, quantity, sum) 
                    VALUES ($1, $2, $3, $4, $5, $6)
                '''

                await conn.execute(
                    query, stat['date'], str(stat['barcode']), stat['warehouseName'],
                    str(stat['nmId']), stat['count'], stat['priceWithDisc']
                )
    finally:
        await close_db_connection(conn)


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