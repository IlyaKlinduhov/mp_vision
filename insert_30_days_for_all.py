from first_insert.first_insert_advert import main_first_advert
from first_insert.first_insert_nmid_skus_stocks_remain import fetch_articles_data
from first_insert.first_insert_orders import main_orders
from first_insert.first_insert_sales import main_sales
from first_insert.first_insert_salesfunel import main_salesfunel
from db.insert_new_user import insert_new_user
import asyncio
from db.get_all_users import get_all_users

async def update_all_users():
    all_users = await get_all_users()

    for user in all_users:
        print(f"Начало работы с {user['user_id']}")
        try:
            await fetch_articles_data(user['token'], user['user_id'])
        finally:
            pass

        try:
            await main_first_advert(user['token'])
        finally:
            pass

        try:
            await main_salesfunel(user['token'])
        finally:
            pass

        try:
            await main_orders(user['token'])
        finally:
            pass
        
        try:
            await main_sales(user['token'])
        finally:
            pass
        
        print(f"Конец работы с {user['user_id']}")

if __name__ == '__main__':
    asyncio.run(update_all_users())
