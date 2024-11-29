import json
import requests
import time
from datetime import datetime


def get_all_adverts(api_key):
    api_url = 'https://advert-api.wildberries.ru/adv/v1/promotion/count'
    max_retries = 20  # Максимальное количество повторных попыток
    headers = {
        'Authorization': api_key  # Функция для получения API ключа
    }

    advert_map = {}

    success = False
    retries = 0
    response_data = None

    while not success and retries < max_retries:
        try:
            response = requests.get(api_url, headers=headers)

            if response.status_code == 200:  # Проверяем, что ответ успешен
                response_data = response.json()
                success = True  # Запрос успешен, выходим из цикла
            else:
                print(f"Error: Response code {response.status_code}. Retrying...")
                retries += 1
                time.sleep(0.2)  # Задержка перед повторной попыткой

        except Exception as e:
            print(f"Error: {str(e)}. Retrying...")
            retries += 1
            time.sleep(0.2)  # Задержка перед повторной попыткой

    if not success:
        return None

    for item in response_data['adverts']:
        if (item['status'] not in [7, 8]) and (item['type'] in [8, 9]):
            adverts = item['advert_list']
            for advert in adverts:
                advert_map[advert['advertId']] = item['type']

    if len(advert_map) > 0:
        return advert_map
    else:
        return None



def get_adverts_stat(advert_map, api_key, date_array):
    main_advert_array = list(advert_map.keys())
    api_url = 'https://advert-api.wildberries.ru/adv/v2/fullstats'
    end_map = {}

    k = 0

    for date in date_array:
        advert_array = main_advert_array.copy()
        while advert_array:
            if k > 0:
                time.sleep(10)
            result = []
            help_array = advert_array[:99]
            advert_array = advert_array[99:]

            for advert in help_array:
                item = {
                    "id": advert,
                    "dates": date
                }
                result.append(item)

            options = {
                'headers': {
                    'Authorization': api_key,
                    'Content-Type': 'application/json'
                },
                'data': json.dumps(result)
            }

            max_retries = 2  # Максимальное количество повторных попыток
            success = False
            retries = 0
            response_data = None

            while not success and retries < max_retries:
                try:
                    response = requests.post(api_url, **options)
                    k+=1
                    if response.status_code in [200]:  # Проверяем, что ответ успешен
                        response_data = response.json()
                        success = True  # Запрос успешен, выходим из цикла
                    else:
                        print(f'Error: Response code {response.status_code}. Retrying...')
                        retries += 1
                        time.sleep(40)  # Задержка перед повторной попыткой

                except Exception as e:
                    print(f'Error: {str(e)}. Retrying...')
                    retries += 1
                    time.sleep(40)

            if not success:
                print(f'Failed to fetch data after {retries} attempts.')
                continue

            for item in response_data:
                advert_id = item.get("advertId")
                for day in item['days']:
                    for app in day['apps']:
                        for nm in app['nm']:
                            nmid = nm['nmId']
                            nm_date = str(day['date'])[:10]
                            key = f'{nmid}{advert_id}{nm_date}'
                            if key in end_map:
                                stat = end_map[key]
                                stat['views'] += nm.get('views', 0)
                                stat['clicks'] += nm.get('clicks', 0)
                                stat['sum'] += nm.get('sum', 0)
                            else:
                                stat = {
                                    'nmid': nmid,
                                    'advertId': advert_id,
                                    'date': datetime.strptime(nm_date, '%Y-%m-%d').date(),
                                    'views': nm.get('views', 0),
                                    'clicks': nm.get('clicks', 0),
                                    'sum': nm.get('sum', 0),
                                    'type': advert_map.get(advert_id)
                                }
                                end_map[key] = stat
            print(f'Получены данные за {date[0]} - {date[-1]}')


    if end_map:
        return end_map
    else:
        return None




# def get_yesterday_advert_map(advert_list):
#     date = datetime.strptime(get_yesterday_date_no_zeros(), '%Y-%m-%d').date()
#     api_url = 'https://advert-api.wildberries.ru/adv/v1/promotion/adverts'
#     max_retries = 5
#     headers = {
#         'Authorization': API_KEY,
#         'Content-Type': 'application/json'
#     }
#
#     success = False
#     retries = 0
#     response_data = None
#     advert_nmid_map = dict()
#
#     while advert_list:  # Пока есть элементы в advert_list
#         batch = advert_list[:50]  # Берем по 50 элементов
#         advert_list = advert_list[50:]  # Уменьшаем список на обработанные элементы
#
#         while not success and retries < max_retries:
#             try:
#                 response = requests.post(api_url, headers=headers, json=batch)  # Отправляем запрос с пачкой данных
#
#                 if response.status_code == 200:
#                     response_data = response.json()
#                     success = True
#                 else:
#                     print(f'Error: Response code {response.status_code}. Retrying...')
#                     retries += 1
#                     time.sleep(0.3)
#
#             except Exception as e:
#                 print(f'Error: {e}. Retrying...')
#                 retries += 1
#                 time.sleep(0.3)
#
#         if not success:
#             print(f'Failed to fetch data after {retries} attempts.')
#             return None
#
#         # Обработка данных из response_data
#         for item in response_data:
#             if item['type'] not in [8, 9]:
#                 continue
#             if item['type'] == 8:
#                 param_name = 'autoParams'
#             if item['type'] == 9:
#                 param_name = 'unitedParams'
#             param = item.get(param_name)
#             if isinstance(param, dict) and 'nms' in param:
#                 for nm in param['nms']:
#                     key = f"{str(nm)}{item['advertId']}"
#                     stat = {
#                         'nmid': nm,
#                         'advertId': item['advertId'],
#                         'views': 0,
#                         'clicks': 0,
#                         'sum': 0,
#                         'date': date
#                     }
#                     advert_nmid_map[key] = stat
#
#         success = False  # Сбрасываем флаг успеха для следующей пачки
#         retries = 0  # Обнуляем счетчик попыток
#
#     return advert_nmid_map if advert_nmid_map else None