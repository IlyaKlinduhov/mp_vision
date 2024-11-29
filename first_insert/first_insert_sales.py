import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.sales import get_month_buyouts
from db.sales import save_buyouts_to_db


async def main_sales(api_key):
    buyouts = get_month_buyouts(api_key)
    if len(buyouts) > 0:
        await save_buyouts_to_db(buyouts)
    else:
        print("No cards to save.")