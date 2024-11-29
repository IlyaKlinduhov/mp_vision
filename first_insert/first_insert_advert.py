import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.advert import  get_adverts_stat, get_all_adverts
from db.advert import save_adverts_to_db
from datetime import datetime, timedelta



async def main_first_advert(api_key):
    advert_map = get_all_adverts(api_key)
    end_map = get_adverts_stat(advert_map, api_key, generate_date_ranges())
    if len(advert_map) > 0:
        await save_adverts_to_db(end_map)
    else:
        print("No cards to save.")


def generate_date_ranges():
    today = datetime.today()
    dates = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(1, 31)]

    first_range = dates[:10]  # с 30 по 20 день
    second_range = dates[10:20]  # с 20 по 10 день
    third_range = dates[20:]  # с 10 по 1 день

    return [first_range, second_range, third_range]

