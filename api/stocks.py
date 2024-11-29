import requests
import time

API_URL = 'https://seller-analytics-api.wildberries.ru/api/v1'

def main_stocks(api_key):
    report_id = generate_stocks_report(api_key)
    if report_id is not None:
        report_status = get_stocks_report_status(report_id, api_key)
        if report_status:
            stocks_report = get_stocks_report(report_id, api_key)
            if len(stocks_report) > 0:
                return stocks_report
    return None

def generate_stocks_report(api_key):
    url = f'{API_URL}/warehouse_remains?groupByBarcode=true'
    headers = {
        'Authorization': api_key,
        'Content-Type': 'application/json'
    }
    retries = 0
    max_retries = 3

    while retries < max_retries:
        response = requests.get(url, headers=headers)
        if response.status_code in [200, 201]:
            return response.json()['data']['taskId']
        else:
            print(f'Error: Response code {response.status_code}. Retrying...')
            retries += 1
            time.sleep(60)

    print('Failed to fetch data after max attempts.')
    return None

def get_stocks_report_status(task_id, api_key):
    url = f'{API_URL}/warehouse_remains/tasks/{task_id}/status'
    headers = {'Authorization': api_key}
    retries = 0
    max_retries = 24

    while retries < max_retries:
        response = requests.get(url, headers=headers)
        if response.status_code == 200 and response.json()['data']['status'] == 'done':
            return True
        else:
            print(f'Error: Response code {response.status_code}. Retrying...')
            retries += 1
            time.sleep(5)

    print('Failed to fetch report status after max attempts.')
    return False

def get_stocks_report(task_id, api_key):
    url = f'{API_URL}/warehouse_remains/tasks/{task_id}/download'
    headers = {'Authorization': api_key}
    retries = 0
    max_retries = 2

    while retries < max_retries:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f'Error: Respons code {response.status_code}. Retrying...')
            retries += 1
            time.sleep(60)

    print('Failed to download report after max attempts.')
    return None