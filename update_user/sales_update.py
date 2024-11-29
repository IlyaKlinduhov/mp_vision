import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.sales import get_yesterday_buyouts
from db.sales import save_buyouts_to_db, delete_yesterday_sales


async def main_sales_update(api_key, user_id):
    buyouts = get_yesterday_buyouts(api_key)
    if len(buyouts) > 0:
        await delete_yesterday_sales(user_id)
        await save_buyouts_to_db(buyouts)
    else:
        print("No cards to save.")