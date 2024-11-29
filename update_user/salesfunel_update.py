import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.salesfunel import get_salesfunel
from db.salesfunel import save_salesfunel_to_db, delete_yesterday_salesfunel
from first_insert.first_insert_salesfunel import generate_date_ranges_salesfunel

async def main_salesfunel(user_id, api_key):
    salesfunel_map = get_salesfunel(api_key, generate_date_ranges_salesfunel(1))
    if len(salesfunel_map) > 0:
        await delete_yesterday_salesfunel(user_id)
        await save_salesfunel_to_db(salesfunel_map)
    else:
        print("No salesfunel to save.")
