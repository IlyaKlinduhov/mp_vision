from datetime import datetime

import requests
from collections import defaultdict
import time
from utils.dates import get_yesterday_date_no_zeros, get_month_ago_date_no_zeros


def get_month_buyouts(api_key):
    date = get_month_ago_date_no_zeros()
    api_url = f'https://statistics-api.wildberries.ru/api/v1/supplier/sales?dateFrom={date}&flag=0'

    max_retries = 5  # Максимальное количество попыток
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
                time.sleep(60)  # Задержка перед повторной попыткой

        except Exception as e:
            print(f'Error: {str(e)}. Retrying...')
            retries += 1
            time.sleep(60)  # Задержка перед повторной попыткой

    if not success:
        print(f'Failed to fetch data after {retries} attempts.')
        return None

    buyouts_map = defaultdict(lambda: {'count': 0, 'forPay': 0})

    for item in response_data:
        trimmed_date = item['date'][:10]
        if (
            item['orderType'] == "Клиентский" and
            datetime.strptime(trimmed_date, '%Y-%m-%d').date() >= datetime.strptime(date, '%Y-%m-%d').date()
        ):
            key = f"{item['warehouseName']}{item['barcode']}{item['saleID'][0]}{trimmed_date}"

            if key in buyouts_map:
                stat = buyouts_map[key]
                stat['count'] += 1
                stat['forPay'] += item['forPay']
                stat['priceWithDisc'] += item['priceWithDisc']
            else:
                buyouts_map[key] = {
                    'flag': item['saleID'][0],
                    'date': datetime.strptime(trimmed_date, '%Y-%m-%d').date(),
                    'nmId': item['nmId'],
                    'brand': item['brand'],
                    'barcode': item['barcode'],
                    'subject': item['subject'],
                    'category': item['category'],
                    'supplierArticle': item['supplierArticle'],
                    'priceWithDisc': item['priceWithDisc'],
                    'forPay': item['forPay'],
                    'warehouseName': item['warehouseName'],
                    'count': 1
                }

    if buyouts_map:
        return dict(buyouts_map)
    else:
        print('No valid data in API response.')
        return None
    


def get_yesterday_buyouts(api_key):
    date = get_yesterday_date_no_zeros()
    api_url = f'https://statistics-api.wildberries.ru/api/v1/supplier/sales?dateFrom={date}&flag=0'

    max_retries = 5  # Максимальное количество попыток
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
                time.sleep(60)  # Задержка перед повторной попыткой

        except Exception as e:
            print(f'Error: {str(e)}. Retrying...')
            retries += 1
            time.sleep(60)  # Задержка перед повторной попыткой

    if not success:
        print(f'Failed to fetch data after {retries} attempts.')
        return None

    buyouts_map = defaultdict(lambda: {'count': 0, 'forPay': 0})

    for item in response_data:
        trimmed_date = item['date'][:10]
        if (
            item['orderType'] == "Клиентский" and
            datetime.strptime(trimmed_date, '%Y-%m-%d').date() == datetime.strptime(date, '%Y-%m-%d').date()
        ):
            key = f"{item['warehouseName']}{item['barcode']}{item['saleID'][0]}{trimmed_date}"

            if key in buyouts_map:
                stat = buyouts_map[key]
                stat['count'] += 1
                stat['forPay'] += item['forPay']
                stat['priceWithDisc'] += item['priceWithDisc']
            else:
                buyouts_map[key] = {
                    'flag': item['saleID'][0],
                    'date': datetime.strptime(trimmed_date, '%Y-%m-%d').date(),
                    'nmId': item['nmId'],
                    'brand': item['brand'],
                    'barcode': item['barcode'],
                    'subject': item['subject'],
                    'category': item['category'],
                    'supplierArticle': item['supplierArticle'],
                    'priceWithDisc': item['priceWithDisc'],
                    'forPay': item['forPay'],
                    'warehouseName': item['warehouseName'],
                    'count': 1
                }

    if buyouts_map:
        return dict(buyouts_map)
    else:
        print('No valid data in API response.')
        return None