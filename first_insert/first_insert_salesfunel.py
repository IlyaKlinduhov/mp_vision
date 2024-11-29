import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.salesfunel import get_salesfunel
from db.salesfunel import save_salesfunel_to_db
from datetime import datetime, timedelta



def generate_date_ranges_salesfunel(count):
    today = datetime.today()
    date_ranges = []

    for i in range(count):
        date_begin = (today - timedelta(days=i+1)).replace(hour=0, minute=0, second=0, microsecond=0)
        date_end = (today - timedelta(days=i+1)).replace(hour=23, minute=59, second=59, microsecond=999999)

        date_ranges.append({
            'begin': date_begin.strftime('%Y-%m-%d %H:%M:%S'),
            'end': date_end.strftime('%Y-%m-%d %H:%M:%S')
        })

    return date_ranges

async def main_salesfunel(api_key):
    salesfunel_map = get_salesfunel(api_key, generate_date_ranges_salesfunel(30))
    if len(salesfunel_map) > 0:
        await save_salesfunel_to_db(salesfunel_map)
    else:
        print("No salesfunel to save.")
