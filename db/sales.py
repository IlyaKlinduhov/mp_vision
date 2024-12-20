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

                warehouse = await conn.fetchval('SELECT warehouse FROM warehouses WHERE warehouse = $1', stat['warehouseName'])
                if warehouse is None:
                    await conn.execute('INSERT INTO warehouses (warehouse) VALUES($1)', stat['warehouseName'])

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

                warehouse = stat['warehouseName']
                if stat['warehouseName'] == 'Алексин':
                    warehouse = 'Тула'

                if stat['warehouseName'] == 'Санкт-Петербург':
                    warehouse = 'Санкт-Петербург Уткина Заводь'

                if stat['warehouseName'] == 'Екатеринбург':
                    warehouse = 'Екатеринбург - Испытателей 14г'

                if stat['warehouseName'] == 'Рязанская обл.':
                    warehouse = 'Рязань (Тюшевское)' 

                if stat['warehouseName'] == 'Виртуальный Комсомольск-на-Амуре':
                    continue
                    # warehouse = 'Хабаровск' 

                if stat['warehouseName'] == 'Виртуальный Краснодар':
                    continue
                    #warehouse = 'Краснодар' 

                

                await conn.execute(
                    query, stat['date'], flag, str(stat['barcode']), warehouse,
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