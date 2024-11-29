from connection import *
from datetime import datetime, timedelta

async def save_buyouts_to_db(buyouts):
    conn = await get_db_connection()
    try:
        async with conn.transaction():
            for buyout in buyouts:
                stat = buyouts.get(buyout)

                nmid = await conn.fetchval('SELECT nmid FROM skus WHERE sku = $1', str(stat['barcode']))

                if nmid is None:
                    continue

                query = '''
                    INSERT INTO sales (date, flag, sku, warehouse, quantity, order_sum, sum_for_pay, nmid) 
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                    ON CONFLICT DO NOTHING 
                '''
                flag = None
                if stat['flag'] == "S":
                    flag = True
                else:
                    flag = False

                await conn.execute(
                    query, stat['date'], flag, str(stat['barcode']), stat['warehouseName'],
                    stat['count'], stat['priceWithDisc'], stat['forPay'], str(stat['nmId'])
                )
    finally:
        await close_db_connection(conn)


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


async def delete_depricated_rows_in_sales():
    today = datetime.now().date()
    depricated_day = today - timedelta(days=31)

    conn = await get_db_connection()
    try:
        await conn.execute('DELETE FROM sales WHERE date <= $1', depricated_day)
    finally:
        await close_db_connection(conn)