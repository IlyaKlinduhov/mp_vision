from connection import *
from db.nmid_and_sku import *
from api.nomenculature import get_report_nomenclature


async def main_update_nmid_sku_for_user(api_key, user_id, categories):
    cards = get_report_nomenclature(api_key)
    if len(cards) > 0 and len(categories) > 0:
        await update_nmid_and_sku_for_user(user_id, cards, categories)
    else:
        print("No cards to save.")


def generate_new_nmid_array(cards):
    new_nmid_array = []
    for card in cards:
        new_nmid_array.append(str(card['nmID']))
    return new_nmid_array


def generate_new_skus_array(cards):
    new_skus_array = []
    for card in cards:
        for size in card['sizes']:
            new_skus_array.append(str(size['skus'][0]))
    return new_skus_array


async def update_nmid_and_sku_for_user(user_id, cards, categories):
    conn = await get_db_connection()

    try:
        prev_nmids = await get_all_nmid_by_user_id(user_id)
        new_nmids = generate_new_nmid_array(cards)
        
        delete_nmid_array = []
        for prev_nmid in prev_nmids:
            if prev_nmid not in new_nmids:
                delete_nmid_array.append(prev_nmid)

        values = []
        sku_values = []
        for card in cards:
            if str(card['nmID']) not in prev_nmids:
                if categories.get(card['subjectID']) is not None:
                    parent_name = categories[card['subjectID']]
                    values.append((
                        str(card['nmID']), card['brand'], card['subjectName'],
                        parent_name, card['vendorCode'], card['title'],
                        card.get('photos', [{'big': 'нет фото'}])[0]['big'], user_id
                    ))
                    

        prev_skus = await get_all_skus_by_user_id(user_id)
        new_skus = generate_new_skus_array(cards)

        delete_skus_array = []
        for prev_sku in prev_skus:
            if prev_sku not in new_skus:
                delete_skus_array.append(prev_sku)

        for card in cards:
            if str(card['nmID']) not in prev_nmids:
                if categories.get(card['subjectID']) is not None:
                    for size in card['sizes']:
                        sku_values.append(
                            (str(size['skus'][0]), str(size['techSize']), str(size['wbSize']), str(card['nmID']))
                        )
        print(values)
        print(sku_values)
        print(delete_nmid_array)
        print(delete_skus_array)  
        
        if (len(delete_nmid_array) > 0):
            await delete_nmid_from_array(delete_nmid_array)

        if (len(delete_skus_array) > 0):
            await delete_skus_from_array(delete_skus_array)

        if (len(values) > 0):
            await insert_nmid_array(values)

        if (len(sku_values) > 0):
            await insert_sku_array(sku_values)

    finally:
        await close_db_connection(conn) 