from connection import *

async def save_data_to_db(cards, categories, user_id):
    conn = await get_db_connection()
    try:
        async with conn.transaction():
            nmids_values = []
            skus_values = []
            for card in cards:
                if categories.get(card['subjectID']) is not None:
                    parent_name = categories[card['subjectID']]

                    nmids_values.append((
                        str(card['nmID']), card['brand'], card['subjectName'],
                        parent_name, card['vendorCode'], card['title'],
                        card.get('photos', [{'big': 'нет фото'}])[0]['big'], user_id
                    ))

                    for size in card['sizes']:
                        skus_values.append(
                            (str(size['skus'][0]), str(size['techSize']), str(size['wbSize']), str(card['nmID']))
                        )
               
                        
            query = '''
                        INSERT INTO nmids (nmID, brand, subject_name, parent_name, vendor_code, title, photo, user_id)
                        VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                        ON CONFLICT (nmID) DO NOTHING
                    '''
                    
            await conn.executemany(
                query, nmids_values
            )

            sku_query = '''
                            INSERT INTO skus (sku, tech_size, wb_size, nmid)
                            VALUES ($1, $2, $3, $4)
                            ON CONFLICT DO NOTHING 
                        '''

            await conn.executemany(
                sku_query, skus_values
            )


    finally:
        await close_db_connection(conn)


async def get_all_nmid_by_user_id(user_id):
    conn = await get_db_connection()
    all_nmid = []
    try:
        all_nmid = [row[0] for row in await conn.fetch('SELECT nmid FROM nmids WHERE user_id = $1', user_id)] 
    finally:
        await close_db_connection(conn)

    return all_nmid


async def get_all_skus_by_user_id(user_id):
    conn = await get_db_connection()
    all_skus = []
    try:
        sku_query = '''
            SELECT sku FROM skus WHERE nmid IN (SELECT nmid FROM nmids WHERE user_id = $1)
        '''
        all_skus = [row[0] for row in await conn.fetch(sku_query, user_id)]
    finally:
        await close_db_connection(conn)

    return all_skus


async def delete_nmid_from_array(nmid_array):
    conn = await get_db_connection()
    try:
        await conn.execute('DELETE FROM nmids WHERE nmid = ANY ($1::varchar(20)[])', nmid_array)
    finally:
        await close_db_connection(conn)


async def delete_skus_from_array(skus_array):
    conn = await get_db_connection()
    try:
        await conn.execute('DELETE FROM skus WHERE sku = ANY ($1::varchar(30)[])', skus_array)
    finally:
        await close_db_connection(conn)


async def insert_nmid_array(nmid_array):
    conn = await get_db_connection()
    try:
        query = '''INSERT INTO nmids (nmID, brand, subject_name, parent_name, vendor_code, title, photo, user_id)
                        VALUES ($1, $2, $3, $4, $5, $6, $7, $8)'''
        await conn.executemany(query, nmid_array)
    finally:
        await close_db_connection(conn)


async def insert_sku_array(sku_array):
    conn = await get_db_connection()
    try:
        query = '''INSERT INTO skus (sku, tech_size, wb_size, nmid)
                            VALUES ($1, $2, $3, $4)'''      
        await conn.executemany(query, sku_array)
    finally:
        await close_db_connection(conn)