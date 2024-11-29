from collections import defaultdict
from datetime import datetime

import time
import requests
from utils.dates import get_yesterday_date_no_zeros, get_month_ago_date_no_zeros


def get_yesterday_orders(api_key):
    date = get_yesterday_date_no_zeros()
    api_url = f'https://statistics-api.wildberries.ru/api/v1/supplier/orders?dateFrom={date}&flag=0'
    max_retries = 5
    headers = {
        'Authorization': api_key,
        'Content-Type': 'application/json'
    }

    success = False
    retries = 0
    response_data = None

    while not success and retries < max_retries:
        try:
            response = requests.get(api_url, headers=headers)

            if response.status_code == 200:
                response_data = response.json()
                success = True
            else:
                print(f'Error: Response code {response.status_code}. Retrying...')
                retries += 1
                time.sleep(60)  # Sleep for 60 seconds before retrying

        except Exception as e:
            print(f'Error: {e}. Retrying...')
            retries += 1
            time.sleep(60)

    if not success:
        print(f'Failed to fetch data after {retries} attempts.')
        return None

    sales_map = defaultdict(lambda: {
        'count': 0,
        'priceWithDisc': 0
    })

    for item in response_data:
        trimmed_date = item['date'][:10]  # Assuming the date format is yyyy-mm-dd...
        # if (
        #     item['orderType'] == 'Клиентский' and
        #     datetime.strptime(trimmed_date, '%Y-%m-%d').date() >= datetime.strptime(date, '%Y-%m-%d').date() and
        #     not item['isCancel']
        # ):
        if (
            item['orderType'] == 'Клиентский' and
            datetime.strptime(trimmed_date, '%Y-%m-%d').date() == datetime.strptime(date, '%Y-%m-%d').date()
        ):
            key = f"{item['warehouseName']}{item['barcode']}{trimmed_date}"
            stat = sales_map[key]
            stat['count'] += 1
            stat['priceWithDisc'] += item['priceWithDisc']
            stat.update({
                'date': datetime.strptime(trimmed_date, '%Y-%m-%d').date(),
                'nmId': item['nmId'],
                'barcode': item['barcode'],
                'brand': item['brand'],
                'subject': item['subject'],
                'category': item['category'],
                'supplierArticle': item['supplierArticle'],
                'warehouseName': item['warehouseName']
            })

    if sales_map:
        return dict(sales_map)
    else:
        return None
    

def get_month_orders(api_key):
    date = get_month_ago_date_no_zeros()
    api_url = f'https://statistics-api.wildberries.ru/api/v1/supplier/orders?dateFrom={date}&flag=0'
    max_retries = 5
    headers = {
        'Authorization': api_key,
        'Content-Type': 'application/json'
    }

    success = False
    retries = 0
    response_data = None

    while not success and retries < max_retries:
        try:
            response = requests.get(api_url, headers=headers)

            if response.status_code == 200:
                response_data = response.json()
                success = True
            else:
                print(f'Error: Response code {response.status_code}. Retrying...')
                retries += 1
                time.sleep(60)  # Sleep for 60 seconds before retrying

        except Exception as e:
            print(f'Error: {e}. Retrying...')
            retries += 1
            time.sleep(60)

    if not success:
        print(f'Failed to fetch data after {retries} attempts.')
        return None

    sales_map = defaultdict(lambda: {
        'count': 0,
        'priceWithDisc': 0
    })

    for item in response_data:
        trimmed_date = item['date'][:10]  # Assuming the date format is yyyy-mm-dd...
        # if (
        #     item['orderType'] == 'Клиентский' and
        #     datetime.strptime(trimmed_date, '%Y-%m-%d').date() >= datetime.strptime(date, '%Y-%m-%d').date() and
        #     not item['isCancel']
        # ):
        if (
            item['orderType'] == 'Клиентский' and
            datetime.strptime(trimmed_date, '%Y-%m-%d').date() >= datetime.strptime(date, '%Y-%m-%d').date()
        ):
            key = f"{item['warehouseName']}{item['barcode']}{trimmed_date}"
            stat = sales_map[key]
            stat['count'] += 1
            stat['priceWithDisc'] += item['priceWithDisc']
            stat.update({
                'date': datetime.strptime(trimmed_date, '%Y-%m-%d').date(),
                'nmId': item['nmId'],
                'barcode': item['barcode'],
                'brand': item['brand'],
                'subject': item['subject'],
                'category': item['category'],
                'supplierArticle': item['supplierArticle'],
                'warehouseName': item['warehouseName']
            })

    if sales_map:
        return dict(sales_map)
    else:
        return None