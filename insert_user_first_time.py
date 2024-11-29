from generate_user import save_random_one_user
from generate_nmid import insert_nmid_for_one_user
from generate_sku import insert_sku_for_one_user
from generate_stocks import save_stocks_for_user_first_time
from generate_orders import insert_orders_by_30_days_for_user
from generate_sales import insert_sales_by_30_days_for_user
from generate_salesfunel import insert_salesfunel_by_30_days_for_user
from generate_adverts import insert_advert_for_one_user_for_30_days
import asyncio
from concurrent.futures import ThreadPoolExecutor
import time

async def insert_into_db_new_user():
    user_id = await save_random_one_user()
    print(f'Начало заполения пользователя {user_id}')
    await insert_nmid_for_one_user(user_id)
    await insert_sku_for_one_user(user_id)
    await save_stocks_for_user_first_time(user_id)
    await insert_orders_by_30_days_for_user(user_id)
    await insert_sales_by_30_days_for_user(user_id)
    await insert_salesfunel_by_30_days_for_user(user_id)
    await insert_advert_for_one_user_for_30_days(user_id)
    print(f'Конец заполнения пользователя {user_id}')


async def main():
    # Создаем ThreadPoolExecutor для работы с потоками
    with ThreadPoolExecutor(max_workers=20) as executor:
        loop = asyncio.get_running_loop()
        
        # Запускаем 50 асинхронных задач в разных потоках
        tasks = [
            loop.run_in_executor(executor, asyncio.run, insert_into_db_new_user())
            for _ in range(1)
        ]
        
        # Ожидаем завершения всех задач
        await asyncio.gather(*tasks)

if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Время выполнения: {elapsed_time:.2f} секунд")



    




    