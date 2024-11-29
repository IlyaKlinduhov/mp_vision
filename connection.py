import os
import asyncpg
from dotenv import load_dotenv
import asyncio

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


semaphore = asyncio.Semaphore(10)  # Устанавливаем максимум 10 параллельных подключений

async def get_db_connection_with_semaphore():
    """Получаем подключение с использованием семафора для ограничения параллельных запросов."""
    async with semaphore:
        return await get_db_connection()

async def get_db_connection():
    conn = await asyncpg.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

async def close_db_connection(conn):
    await conn.close()