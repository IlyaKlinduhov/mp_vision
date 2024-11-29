import datetime

def get_yesterday_date_no_zeros():
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    year = yesterday.year
    month = str(yesterday.month).zfill(2)  # Добавляем ведущий ноль, если необходимо
    day = str(yesterday.day).zfill(2)  # Добавляем ведущий ноль, если необходимо
    return f"{year}-{month}-{day}"

def get_month_ago_date_no_zeros():
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=30)
    year = yesterday.year
    month = str(yesterday.month).zfill(2)  # Добавляем ведущий ноль, если необходимо
    day = str(yesterday.day).zfill(2)  # Добавляем ведущий ноль, если необходимо
    return f"{year}-{month}-{day}"
