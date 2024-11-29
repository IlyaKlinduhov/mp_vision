from connection import *
from generate_nmid import update_nmid_and_sku_for_user
from generate_stocks import update_stocks_for_user
from generate_orders import delete_depricated_rows_in_orders, update_orders_for_user
from generate_sales import delete_depricated_rows_in_sales, update_sales_for_user
from generate_salesfunel import delete_depricated_rows_in_salesfunel, update_salesfunel_for_user
from generate_adverts import delete_depricated_rows_in_adverts, update_advert_for_user
import asyncio
import time


async def update_all_users():
    start_time = time.time()
    i = 1
    while i<2:
        print(f'{i} круг обновления начат')
        
        # Устанавливаем соединение с базой данных
        conn = await get_db_connection()

        # Удаляем устаревшие строки
        await delete_depricated_rows_in_adverts()
        await delete_depricated_rows_in_salesfunel()
        await delete_depricated_rows_in_orders()
        await delete_depricated_rows_in_sales()

        # Получаем всех пользователей
        all_users = [row[0] for row in await conn.fetch('SELECT user_id FROM users')]

        # Создаём задачи для каждого пользователя
        tasks = []
        for user_id in all_users:
            
            # Создаём задачу для обновления пользователя
            tasks.append(
                update_user_data(user_id)
            )

        # Параллельно выполняем задачи обновления данных для всех пользователей
        await asyncio.gather(*tasks)
        
        print(f'{i} круг обновления закончен')
        i += 1
    
    # Замеряем и выводим время выполнения
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Время выполнения: {elapsed_time:.2f} секунд")

async def update_user_data(user_id):
    """Функция обновления данных для одного пользователя"""
    print(f'Начало работы с user = {user_id}')
    await update_nmid_and_sku_for_user(user_id)
    await update_stocks_for_user(user_id)
    await update_orders_for_user(user_id)
    await update_sales_for_user(user_id)
    await update_salesfunel_for_user(user_id)
    await update_advert_for_user(user_id)
    print(f'Конец работы с user = {user_id}')
            


if __name__ == '__main__':
    asyncio.run(update_all_users())