from connection import *

async def delete_remains_for_user(user_id):
    conn = await get_db_connection()
    try:
        query = '''
            DELETE FROM remains WHERE nmid IN (SELECT nmid FROM nmids WHERE user_id = $1)
        '''
        await conn.execute(query, user_id)
    finally:
        await close_db_connection(conn)

async def save_stocks_to_db(stocks):
    conn = await get_db_connection()
    try:
        async with conn.transaction():
            values = []
            for stock in stocks:
                values.append((stock['inWayFromClient'], stock['inWayToClient'], stock['barcode']))

            query = '''
                    UPDATE skus 
                    SET in_way_from_client = $1, in_way_to_client = $2
                    WHERE sku = $3
                '''

            await conn.executemany(query, values)
    finally:
        await close_db_connection(conn)



async def save_remains_to_db(stocks):
    conn = await get_db_connection()
    try:
        async with conn.transaction():
            values = []
            for stock in stocks:
                for warehouse in stock['warehouses']:
                    nmid = await conn.fetchval('SELECT nmid FROM skus WHERE sku = $1', str(stock['barcode']))

                    if nmid is not None:
                        values.append((str(stock['barcode']), warehouse['warehouseName'], nmid, warehouse.get('quantity', 0)))

            query = '''
                INSERT INTO remains (sku, warehouse, nmid, quantity) 
                VALUES ($1::varchar(30), $2, $3, $4)
                ON CONFLICT DO NOTHING 
            '''

            await conn.executemany(
                query, values
            )

    finally:
        await close_db_connection(conn)


