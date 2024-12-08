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

                warehouse = await conn.fetchval('SELECT warehouse FROM warehouses WHERE warehouse = $1', stat['warehouseName'])
                if warehouse is None:
                    await conn.execute('INSERT INTO warehouses (warehouse) VALUES($1)', stat['warehouseName'])

                query = '''
                    INSERT INTO orders (date, sku, warehouse, nmid, quantity, sum) 
                    VALUES ($1, $2, $3, $4, $5, $6)
                '''

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
                    query, stat['date'], str(stat['barcode']), warehouse,
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