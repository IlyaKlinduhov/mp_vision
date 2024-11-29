import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import asyncio
from api.orders import get_month_orders
from db.orders import save_orders_to_db


async def main_orders(api_key):
    orders = get_month_orders(api_key)
    if len(orders) > 0:
        await save_orders_to_db(orders)
    else:
        print("No cards to save.")
