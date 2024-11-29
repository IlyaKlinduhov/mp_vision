import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.advert import  get_adverts_stat, get_all_adverts
from db.advert import save_adverts_to_db, delete_yesterday_adverts
from datetime import datetime, timedelta


async def main_update_advert(user_id, api_key):
    advert_map = get_all_adverts(api_key)
    end_map = get_adverts_stat(advert_map, api_key, get_yesterday_date_no_zeros())
    if len(advert_map) > 0:
        await delete_yesterday_adverts(user_id)
        await save_adverts_to_db(end_map)
    else:
        print("No cards to save.")


def get_yesterday_date_no_zeros():
    today = datetime.today()
    date = (today - timedelta(days=1)).strftime('%Y-%m-%d')
    return [[date]]
