from connection import * 
from api.stocks import main_stocks
from db.stocks_remains import delete_remains_for_user, save_stocks_to_db, save_remains_to_db


async def update_stocks_for_user(user_id, api_key):
    stocks = main_stocks(api_key)
    if stocks:
        await delete_remains_for_user(user_id)
        await save_stocks_to_db(stocks)
        await save_remains_to_db(stocks)
    else:
        print("No stocks to save.")

