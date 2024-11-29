import time
from datetime import datetime, timedelta
from time import sleep
import requests


def get_salesfunel(api_key, date_ranges):
    salesfunel_map = dict()
    k = 0
    for date_range in date_ranges:
        api_url = 'https://seller-analytics-api.wildberries.ru/api/v2/nm-report/detail'
        max_retries = 2

        request_body = {
            'period': {
                'begin': date_range['begin'],
                'end': date_range['end']
            },
            'page': 1
        }

        headers = {
            'Authorization': api_key,
            'Content-Type': 'application/json'
        }

        success = False
        retries = 0

        if k > 0:
            sleep(20)

        while not success and retries < max_retries:
            is_next_page = True
            try:
                while is_next_page:
                    response = requests.post(api_url, headers=headers, json=request_body)
                    k+=1
                    if response.status_code == 200:
                        response_data = response.json()
                        is_next_page = response_data['data']['isNextPage']

                        if not is_next_page:
                            success = True
                        else:
                            request_body['page'] += 1

                        for card in response_data['data']['cards']:
                            selected_statistics = card['statistics']['selectedPeriod']
                            trimmed_date = date_range['begin'][:10]
                            key =f'{trimmed_date}{card["nmID"]}'
                            stat = {
                                'nmID': card['nmID'],
                                'date': datetime.strptime(trimmed_date, '%Y-%m-%d').date(),
                                'openCardCount': selected_statistics['openCardCount'],
                                'addToCartCount': selected_statistics['addToCartCount'],
                                'addToCartPercent': selected_statistics['conversions']['addToCartPercent'],
                            }
                            salesfunel_map[key] = stat

                    else:
                        print(f'Error: Response code {response.status_code}. Retrying...')
                        retries += 1
                        time.sleep(60)


            except Exception as e:
                print(f'Error: {e}. Retrying...')
                retries += 1
                time.sleep(60)

        if not success:
            print(f'Failed to fetch data after {retries} attempts. Date {date_range["begin"]}')
            continue
        else:
            print(f'Получены данные за {date_range["begin"]} - {date_range["end"]}')

    if salesfunel_map:
        return salesfunel_map
    else:
        return None




