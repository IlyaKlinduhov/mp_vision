from db.advert import delete_depricated_rows_in_adverts
from db.salesfunel import delete_depricated_rows_in_salesfunel
from db.orders import delete_depricated_rows_in_orders
from db.sales import delete_depricated_rows_in_sales

from update_user.advert_update import main_update_advert
from update_user.nmid_skus_update import main_update_nmid_sku_for_user
from update_user.sales_update import main_sales_update
from update_user.salesfunel_update import main_salesfunel
from update_user.stocks_remains_update import update_stocks_for_user
from update_user.update_orders import main_orders

from db.get_all_users import get_all_users
from api.categories import get_all_categories

import asyncio

async def update_all_users():
    all_users = await get_all_users()

    categories = get_all_categories(all_users[0]['token'])

    try:
        await delete_depricated_rows_in_salesfunel()
        await delete_depricated_rows_in_adverts()
        await delete_depricated_rows_in_orders()
        await delete_depricated_rows_in_sales()
    finally:
        pass

    for user in all_users:
        print(f"Начало работы с user {user['user_id']}")
        try:
            await main_update_nmid_sku_for_user(user['token'], user['user_id'], categories)
        finally:
            pass

        try:
            await main_update_advert(user['user_id'], user['token'])
        finally:
            pass

        try:
            await main_salesfunel(user['user_id'], user['token'])
        finally:
            pass

        try:
            await main_sales_update(user['token'], user['user_id'])
        finally:
            pass

        try:
            await main_orders(user['token'], user['user_id'])
        finally:
            pass

        print(f"Конец работы с user {user['user_id']}")


if __name__ == '__main__':
    import asyncio

    async def main():
        while True:
            await update_all_users()
            print("Ожидание перед следующим запуском...")
            await asyncio.sleep(10)  

    asyncio.run(main())
