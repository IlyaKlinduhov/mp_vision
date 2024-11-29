import requests
import time


def get_report_nomenclature(api_key):
    api_url = "https://content-api.wildberries.ru/content/v2/get/cards/list"

    all_cards = []
    retries = 0
    has_more = True

    # Изначально cursor содержит только limit
    cursor = {
        'limit': 100
    }

    while has_more and retries < 3:
        try:
            # Тело запроса
            request_body = {
                'settings': {
                    'cursor': cursor,
                    'filter': {
                        'withPhoto': -1
                    }
                }
            }

            # Выполняем запрос
            response = requests.post(
                api_url,
                headers={
                    'Authorization': api_key,
                    'Content-Type': 'application/json'
                },
                json=request_body,
            )

            # Проверяем код ответа
            if response.status_code == 200:
                response_data = response.json()

                # Добавляем карточки в общий список
                all_cards.extend(response_data.get('cards', []))

                # Если карточек меньше лимита, прекращаем запросы
                if len(response_data.get('cards', [])) < cursor['limit']:
                    has_more = False
                else:
                    # Обновляем cursor для следующего запроса (добавляем nmID и updatedAt)
                    last_card = response_data['cards'][-1]
                    cursor['updatedAt'] = last_card['updatedAt']
                    cursor['nmID'] = last_card['nmID']

            else:
                # Логируем ошибку и повторяем запрос
                print(f"Error: Response code {response.status_code}. Retrying...")
                retries += 1
                time.sleep(0.5)  # Задержка перед повторной попыткой

        except Exception as e:
            # Логируем и повторяем запрос при ошибке
            print(f"Error: {e}. Retrying...")
            retries += 1
            time.sleep(0.5)  # Задержка перед повторной попыткой

    # Если после 3 попыток данные не были получены
    if retries >= 3:
        print("Failed to fetch data after 3 attempts.")
        return None

    # Возвращаем результат
    return all_cards if all_cards else None