import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.orders import get_yesterday_orders
from db.orders import save_orders_to_db, delete_yesterday_orders


async def main_orders(api_key, user_id):
    orders = get_yesterday_orders(api_key)
    if len(orders) > 0:
        await delete_yesterday_orders(user_id)
        await save_orders_to_db(orders)
    else:
        print("No cards to save.")
