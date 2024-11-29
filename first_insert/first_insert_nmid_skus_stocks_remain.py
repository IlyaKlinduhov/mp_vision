from api.categories import get_all_categories
from api.nomenculature import get_report_nomenclature
from api.stocks import main_stocks
from db.nmid_and_sku import save_data_to_db
from db.stocks_remains import *

async def fetch_articles_data(api_key, user_id):
    cards = get_report_nomenclature(api_key)
    categories = get_all_categories(api_key)
    stocks = main_stocks(api_key)
    if len(cards) > 0 and len(categories) > 0:
        await save_data_to_db(cards, categories, user_id)
    else:
        print("No cards to save.")

    if stocks:
        await save_stocks_to_db(stocks)
        await save_remains_to_db(stocks)
    else:
        print("No stocks to save.")