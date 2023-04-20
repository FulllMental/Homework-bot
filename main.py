import logging
import os
import time

import requests
import telegram
from dotenv import load_dotenv


def get_last_attempt(dvmn_token, timeout, timestamp):
    logging.warning("Getting the last attempts...")
    url = 'https://dvmn.org/api/long_polling/'
    headers = {
        'Authorization': f'Token {dvmn_token}',
    }
    params = {
        'timestamp': timestamp,
    }
    response = requests.get(url, headers=headers, timeout=timeout, params=params)
    response.raise_for_status()
    return response.json()


def get_last_timestamp(dvmn_token):
    logging.warning("Getting the last timestamp...")
    url = 'https://dvmn.org/api/user_reviews/'
    headers = {
        'Authorization': f'Token {dvmn_token}'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()['results'][0]['timestamp']


def send_telegram_message(telegram_token, chat_id, last_attempt):
    logging.warning("Sending telegram message...")
    for attempt in last_attempt['new_attempts']:
        lesson_url = attempt['lesson_url']
        lesson_title = attempt['lesson_title']
        if attempt['is_negative']:
            text = f'У вас проверили работу "{lesson_title}".\n\n' \
                   f'К сожалению, в работе нашлись ошибки.\n' \
                   f'Ссылка: {lesson_url}'
        else:
            text = f'У вас проверили работу {lesson_title}\n\n' \
                   f'Преподавателю всё понравилось, можно приступать к следующему уроку!'
        bot = telegram.Bot(token=telegram_token)
        bot.send_message(chat_id=chat_id, text=text)


if __name__ == '__main__':
    load_dotenv()
    dvmn_token = os.getenv('DVMN_TOKEN')
    timeout = int(os.getenv('TIMEOUT'))
    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('CHAT_ID')
    timestamp = get_last_timestamp(dvmn_token)
    while True:
        try:
            last_attempt = get_last_attempt(dvmn_token, timeout, timestamp)
            send_telegram_message(telegram_token, chat_id, last_attempt)
            timestamp = last_attempt['last_attempt_timestamp']
        except requests.exceptions.ReadTimeout:
            pass
        except requests.exceptions.ConnectionError:
            logging.warning("It's seems you have some connection issues...\nTrying to reconnect...")
            time.sleep(10)
