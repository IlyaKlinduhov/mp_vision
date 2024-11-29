import requests
import time

def get_all_categories(api_key):
    api_url = 'https://content-api.wildberries.ru/content/v2/object/all?limit='

    retries = 0
    has_more = True
    limit = 1000
    offset = 0
    category_map = {}

    while has_more and retries < 3:
        try:
            headers = {
                'Authorization': api_key,
                'Content-Type': 'application/json'
            }

            response = requests.get(f'{api_url}{limit}&offset={offset}', headers=headers)

            if response.status_code == 200:
                response_data = response.json()

                for card in response_data['data']:
                    category_map[card['subjectID']] = card['parentName']

                if len(response_data['data']) < limit:
                    has_more = False
                else:
                    offset += 1000
            else:
                print(f'Error: Response code {response.status_code}. Retrying...')
                retries += 1
                time.sleep(1)

        except Exception as e:
            print(f'Error: {e}. Retrying...')
            retries += 1
            time.sleep(1)

    if retries >= 3:
        print('Failed to fetch data after 3 attempts.')
        return None

    if category_map:
        return category_map
    else:
        print('Invalid data from API.')
        return None