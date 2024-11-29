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
        asyncio.run(create_new_user('dima_tret', 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjQwODAxdjEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTczOTc0NDA1NSwiaWQiOiI4YjZlYmMwZC0wZTZkLTQ4ZjQtYTE0OC0yZTUxMGVjYTQ0MTEiLCJpaWQiOjIxNjYzNDM3LCJvaWQiOjI5NDUzOSwicyI6MTA3Mzc1MDAxNCwic2lkIjoiN2FlZTlkMmItMjJhZS00OGU2LWI0MTktOGRlMDU2NjI1ZDQ3IiwidCI6ZmFsc2UsInVpZCI6MjE2NjM0Mzd9.QOPB0_Poip9xjPwzwoUrnKXzp5Yv3uEEe-1c1xZlSkwhijYYsSU1bSMoH1KvAt3NQGLWRg_2axS_knUyN8mL0Q'))

# if __name__ == '__main__':
#         asyncio.run(main_first_advert('eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjQwODAxdjEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTczOTc0NDA1NSwiaWQiOiI4YjZlYmMwZC0wZTZkLTQ4ZjQtYTE0OC0yZTUxMGVjYTQ0MTEiLCJpaWQiOjIxNjYzNDM3LCJvaWQiOjI5NDUzOSwicyI6MTA3Mzc1MDAxNCwic2lkIjoiN2FlZTlkMmItMjJhZS00OGU2LWI0MTktOGRlMDU2NjI1ZDQ3IiwidCI6ZmFsc2UsInVpZCI6MjE2NjM0Mzd9.QOPB0_Poip9xjPwzwoUrnKXzp5Yv3uEEe-1c1xZlSkwhijYYsSU1bSMoH1KvAt3NQGLWRg_2axS_knUyN8mL0Q'))
