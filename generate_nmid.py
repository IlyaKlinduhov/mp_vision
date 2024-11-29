from faker import Faker
import random
import string
from connection import *
from generate_user import *
from generate_sku import *
import asyncio
from generate_sku import wb_size_arr, tech_size_arr, generateSku

additional_words = [
    "премиум",
    "эконом",
    "для дома",
    "уникальные",
    "инновационные",
    "модные",
    "разнообразные",
    "удобные"
]

title_phrases = [
    "Лучшее качество",
    "Супер акция",
    "Ограниченное предложение",
    "Проверено временем",
    "Невероятная цена",
    "Доставка по всей стране",
    "Купите сейчас и сэкономьте",
    "Только сегодня",
    "Назад в СССР",
    "NESTLED HOME",
    "#ДИМАКРИВОЗУБ"
]



fake = Faker()

def generate_brand_name():
    word1 = fake.word()
    word2 = fake.company_suffix()
    brand_name = f"{word1.capitalize()} {word2.capitalize()}"
    return brand_name

def generate_brand_arr(k):
    arr = []
    for i in range(k):
        arr.append(generate_brand_name())
    return arr

def generate_parents_arr(k):
    products = []
    with open('res/products.txt', 'r', encoding='utf-8') as file:
        products = [line.strip() for line in file if line.strip()]
    return random.sample(products, k)

def generate_nmid():
    first_digit = random.choice(string.digits[1:]) 
    other_digits = ''.join(random.choice(string.digits) for _ in range(8))  
    return first_digit + other_digits

async def insert_nmid_for_one_user(user_id):

    conn = await get_db_connection()
    try:
        all_brands = generate_brand_arr(random.randint(2, 6))
        all_parents = generate_parents_arr(random.randint(1, 10))
        for i in range(random.randint(10, 60)):
            nmid = generate_nmid()
            brand = random.choice(all_brands)
            parent = random.choice(all_parents)
            vendor_code = f'{random.choice(['seller', 'продавец'])} {parent}'
            subject_name = f'{random.choice(additional_words)} {parent}'
            title = f'{subject_name} {random.choice(title_phrases)}'
            photo = f'{nmid}.jpg'

            query = '''INSERT INTO nmids (nmID, brand, subject_name, parent_name, vendor_code, title, photo, user_id)
                        VALUES ($1, $2, $3, $4, $5, $6, $7, $8)'''
            
            await conn.execute(query, nmid, brand, subject_name, parent, vendor_code, title, photo, int(user_id))
    finally:
        await close_db_connection(conn)



def generate_new_nmid_array(prev_array):
    new_array = []
    for nmid in prev_array:
        r = random.uniform(0, 1)
        if r > 0.96:
            if r <= 0.98:
                new_array.append(generate_nmid())
        else:
            new_array.append(nmid)
    return new_array




async def update_nmid_and_sku_for_user(user_id):
    conn = await get_db_connection_with_semaphore()

    try:
        prev_nmids = [row[0] for row in await conn.fetch('SELECT nmid FROM nmids WHERE user_id = $1', user_id)]
        new_nmids = generate_new_nmid_array(prev_nmids)
        
        delete_array = []
        for prev_nmid in prev_nmids:
            if prev_nmid not in new_nmids:
                delete_array.append(prev_nmid)

        all_brands = generate_brand_arr(random.randint(2, 6))
        all_parents = generate_parents_arr(random.randint(1, 10))
        values = []
        sku_values = []
        for new_nmid in new_nmids:
            if new_nmid not in prev_nmids:
                brand = random.choice(all_brands)
                parent = random.choice(all_parents)
                vendor_code = f'{random.choice(['seller', 'продавец'])} {parent}'
                subject_name = f'{random.choice(additional_words)} {parent}'
                title = f'{subject_name} {random.choice(title_phrases)}'
                photo = f'{new_nmid}.jpg'
                values.append((new_nmid, brand, subject_name, parent, vendor_code, title, photo, user_id))
                
                if random.uniform(0, 1) < 0.4:
                    sku_count = 1
                else:
                    sku_count = random.randint(2, 4)
                
                for i in range(sku_count):                    
                    sku_values.append((generateSku(), random.choice(tech_size_arr), random.choice(wb_size_arr), new_nmid))

        if (len(delete_array) > 0):
            await conn.execute('DELETE FROM nmids WHERE nmid = ANY ($1::varchar(20)[])', delete_array)

        if (len(values) > 0):
            query = '''INSERT INTO nmids (nmID, brand, subject_name, parent_name, vendor_code, title, photo, user_id)
                        VALUES ($1, $2, $3, $4, $5, $6, $7, $8)'''
            await conn.executemany(query, values)

        if (len(sku_values) > 0):
            query = '''INSERT INTO skus (sku, tech_size, wb_size, nmid)
                            VALUES ($1, $2, $3, $4)'''      
            await conn.executemany(query, sku_values)

    finally:
        await close_db_connection(conn) 


        

if __name__ == '__main__':
    user_id = asyncio.run(save_random_one_user())
    asyncio.run(insert_nmid_for_one_user(user_id))
    asyncio.run(insert_sku_for_one_user(user_id))