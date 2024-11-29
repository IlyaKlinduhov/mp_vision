from connection import *
import random
import string
from generate_orders import get_last_30_days
import asyncio
from datetime import datetime, timedelta

def generate_advert():
    first_digit = random.choice(string.digits[1:]) 
    other_digits = ''.join(random.choice(string.digits) for _ in range(8))  
    return first_digit + other_digits

async def insert_advert_for_one_user_for_30_days(user_id):
    conn = await get_db_connection()

    dates = get_last_30_days()

    try:
        nmid_rows = await conn.fetch('SELECT nmid FROM nmids WHERE user_id = $1', user_id)

        nmids_array = [row[0] for row in nmid_rows]

        advert_array_lenght = len(nmids_array) * 2 // 3

        advert_dict = {}

        for i in range(advert_array_lenght):
            advert_dict[generate_advert()] = random.choice(nmids_array)

        values = []

        for date in dates:
            for key, value in advert_dict.items():
                views = random.randint(100, 4400)
                clicks = random.randint(10, views // 5)
                sum = views * random.randint(1, 4)
                if random.uniform(0, 1) < 0.9:
                    values.append((date, key, value, views, clicks ,sum))

        query = '''
                    INSERT INTO advert (date, advertid, nmid, views, clicks, sum)
                    VALUES ($1, $2, $3, $4, $5, $6);
                '''
        await conn.executemany(query, values)
        

    finally:
        await close_db_connection(conn)



async def insert_advert_for_one_user_for_yesterday(user_id):
    conn = await get_db_connection_with_semaphore()
    try:
        yesterday = datetime.now().date() - timedelta(days=1)
        unique_rows = await conn.fetch(
            '''
                SELECT DISTINCT a.advertid, n.nmid
                FROM advert a
                JOIN nmids n ON n.nmid = a.nmid
                WHERE n.user_id = $1
            ''', user_id
        )

        nmids = [row[1] for row in unique_rows]

        values = []
        for row in unique_rows:
            views = random.randint(100, 4400)
            clicks = random.randint(10, views // 5)
            sum = views * random.randint(1, 4)

            random_value = random.uniform(0, 1)
            if random_value < 0.8:
                values.append((yesterday, row[0], row[1], views, clicks ,sum))
            elif random_value < 0.9:
                values.append((yesterday, generate_advert(), random.choice(nmids), views, clicks ,sum))

        query = '''
                    INSERT INTO advert (date, advertid, nmid, views, clicks, sum)
                    VALUES ($1, $2, $3, $4, $5, $6);
                '''
        await conn.executemany(query, values)
    finally:
        await close_db_connection(conn)



async def delete_yesterday_adverts(user_id):
    yesterday = datetime.now().date() - timedelta(days=1)

    conn = await get_db_connection_with_semaphore()
    try:
        await conn.execute(
            'DELETE FROM advert WHERE date = $1 AND nmid IN (SELECT nmid FROM nmids WHERE user_id = $2)',
            yesterday, user_id
            )
    finally:
        await close_db_connection(conn)


    
async def update_advert_for_user(user_id):
    await delete_yesterday_adverts(user_id)
    await insert_advert_for_one_user_for_yesterday(user_id)



async def delete_depricated_rows_in_adverts():
    today = datetime.now().date()
    depricated_day = today - timedelta(days=31)

    conn = await get_db_connection()
    try:
        await conn.execute('DELETE FROM advert WHERE date <= $1', depricated_day)
    finally:
        await close_db_connection(conn)



if __name__ == '__main__':
    asyncio.run(insert_advert_for_one_user_for_yesterday(30))