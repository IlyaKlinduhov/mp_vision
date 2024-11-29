import random
from connection import * 
import asyncio

warehouses = [
    'Коледино', 'Тула', 'Электросталь', 'Казань', 'Екатеринбург - Испытателей 14г', 'Невинномысск',
    'Обухово СГТ', 'Голицыно СГТ', 'Радумля СГТ', 'Шушары СГТ', 'Чашниково', 'СЦ Брест', 'Маркетплейс',
    'Подольск 4', 'Атакент', 'Рязань (Тюшевское)', 'Астана Карагандинское шоссе', 'Екатеринбург - Перспективный 12',
    'Краснодар', 'Чехов 2', 'Белая дача', 'Подольск', 'Санкт-Петербург Уткина Заводь', 'Хабаровск', 'Белые Столбы',
    'Новосибирск', 'СЦ Байсерке', 'Актобе', 'СЦ Хабаровск', 'СГТ Внуково', 'Маркетплейс СГТ', 'Иваново',
    'СЦ Кузнецк', 'Минск', 'Обухово 2', 'Котовск', 'СЦ Ижевск', 'СЦ Барнаул', 'Вёшки', 'Новосемейкино',
    'Волгоград', 'Пушкино', 'Обухово', 'Чехов 1', 'СЦ Шушары', 'Крыловская', 'Подольск 3', 'Радумля 1',
    'Санкт-Петербург Шушары', 'Остальные'
]

async def save_stocks_for_one_barcode(barcode, conn):
    try:
        random_warehouses = random.sample(warehouses, random.randint(2, 10))
        total_quantity = 0

        nmids = await conn.fetch('SELECT nmid FROM skus WHERE sku = $1;', barcode)
        nmid = nmids[0][0]

        await conn.execute('DELETE FROM remains WHERE nmid = $1;', nmid)

        values = []
        for warehouse in random_warehouses:
            quantity = random.randint(1, 100)
            total_quantity += quantity
            values.append((quantity, warehouse, nmid, barcode))

        warehouse_query = '''
            INSERT INTO remains (quantity, warehouse, nmid, sku)
            VALUES ($1, $2, $3, $4)
        '''
        await conn.executemany(warehouse_query, values)

        in_way_to_client_count = random.randint(total_quantity // 2, total_quantity - 2)
        in_way_from_client_count = total_quantity - in_way_to_client_count

        await conn.execute(
            '''
            UPDATE skus
            SET in_way_to_client = $1, in_way_from_client = $2
            WHERE sku = $3
            ''',
            in_way_to_client_count, in_way_from_client_count, barcode
        )
    finally:
        pass

async def save_stocks_for_user(user_id, conn):
    try:
        query = '''
                    SELECT sku FROM skus WHERE nmid IN (SELECT nmid FROM nmids WHERE user_id = $1)
                '''
        
        rows = await conn.fetch(query, user_id)

        skus = [row[0] for row in rows]

        for sku in skus:
            await save_stocks_for_one_barcode(sku, conn)
    finally:
        await close_db_connection(conn)

async def delete_stocks_for_user(user_id):
    conn = await get_db_connection_with_semaphore()
    try:
        query = '''
                    DELETE FROM remains WHERE nmid IN (SELECT nmid FROM nmids WHERE user_id = $1)
                '''
        await conn.execute(query, user_id)
    finally:
        await close_db_connection(conn)

async def save_stocks_for_user_first_time(user_id):
    conn = await get_db_connection()
    await save_stocks_for_user(user_id, conn)

async def update_stocks_for_user(user_id):
    await delete_stocks_for_user(user_id)
    conn = await get_db_connection_with_semaphore()
    await save_stocks_for_user(user_id, conn)


if __name__ == '__main__':
    asyncio.run(save_stocks_for_user(30))
    