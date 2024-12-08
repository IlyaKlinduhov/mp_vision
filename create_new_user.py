from first_insert.first_insert_advert import main_first_advert
from first_insert.first_insert_nmid_skus_stocks_remain import fetch_articles_data
from first_insert.first_insert_orders import main_orders
from first_insert.first_insert_sales import main_sales
from first_insert.first_insert_salesfunel import main_salesfunel
from db.insert_new_user import insert_new_user
import asyncio

async def create_new_user(login, token):
    user_id = await insert_new_user(login, token)
    print(f"Начало работы с {user_id}")
    await fetch_articles_data(token, user_id)
    await main_first_advert(token)
    await main_salesfunel(token)
    await main_orders(token)
    await main_sales(token)
    print(f"Конец работы с {user_id}")

if __name__ == '__main__':
        asyncio.run(create_new_user('dima_tret', ''))
