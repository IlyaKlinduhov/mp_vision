from faker import Faker
import random
import string
from connection import *

fake = Faker("ru_Ru")

def generate_name():
    while True:
        first_name = fake.first_name()
        last_name = fake.last_name()
        full_name = f"{first_name} {last_name}"
        
        if len(full_name) <= 50:
            return full_name

def generate_random_sequence(length=100):
    characters = string.ascii_letters + string.digits 
    return ''.join(random.choice(characters) for _ in range(length))


async def save_random_users():
    conn = await get_db_connection()
    try:
        async with conn.transaction():
           query = '''INSERT INTO users (login, token)
                VALUES ($1, $2)
            '''
           
           for i in range(20):
                await conn.execute(
                    query, generate_name(), generate_random_sequence() 
                )
    finally:
        await close_db_connection(conn)

async def save_random_one_user():
    conn = await get_db_connection()
    user_id = None
    try:
        async with conn.transaction():
            query = '''INSERT INTO users (login, token)
                       VALUES ($1, $2)
                       RETURNING user_id'''
           
            user_id = await conn.fetchval(query, generate_name(), generate_random_sequence())
    finally:
        await close_db_connection(conn)
    
    return user_id