import random
import string
from connection import *

tech_size_arr = [str(i) for i in range(50, 60)]

wb_size_arr = ['XXS', 'XS', 'S', 'M', 'L', 'XL', 'XXL']

def generateSku():
    first_digit = random.choice(string.digits[1:]) 
    other_digits = ''.join(random.choice(string.digits) for _ in range(12))  
    return first_digit + other_digits

async def insert_sku_for_one_user(user_id):
    conn = await get_db_connection()
    try:
        query = '''SELECT nmid FROM nmids 
                    WHERE user_id = $1'''
           
        rows = await conn.fetch(query, user_id)

        nmids = [row[0] for row in rows]

        for nmid in nmids:

            if random.uniform(0, 1) < 0.4:
                sku_count = 1
            else:
                sku_count = random.randint(2, 4)
            
            for i in range(sku_count):
                query = '''INSERT INTO skus (sku, tech_size, wb_size, nmid)
                            VALUES ($1, $2, $3, $4)'''
                
                await conn.execute(query, generateSku(), random.choice(tech_size_arr), random.choice(wb_size_arr), nmid)
    finally:
        await close_db_connection(conn)

