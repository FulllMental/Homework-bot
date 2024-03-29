import logging
import os
import textwrap
import time

import requests
import telegram
from dotenv import load_dotenv

logger = logging.getLogger('MyLogsHandler')


class LogsHandler(logging.Handler):
    def __init__(self, tg_chat_id, telegram_token):
        super().__init__()
        self.chat_id = tg_chat_id
        self.token = telegram_token

    def emit(self, record):
        log_entry = self.format(record)
        bot = telegram.Bot(token=self.token)
        bot.send_message(chat_id=self.chat_id, text=textwrap.dedent(log_entry))


def get_last_attempt(dvmn_token, dvmn_api_timeout, timestamp):
    logging.warning("Getting the last attempts...")
    url = 'https://dvmn.org/api/long_polling/'
    headers = {
        'Authorization': f'Token {dvmn_token}',
    }
    params = {
        'timestamp': timestamp,
    }
    response = requests.get(url, headers=headers, timeout=dvmn_api_timeout, params=params)
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


def send_telegram_message(telegram_token, tg_chat_id, last_attempt):
    logging.warning("Sending telegram message...")
    for attempt in last_attempt['new_attempts']:
        lesson_url = attempt['lesson_url']
        lesson_title = attempt['lesson_title']
        if attempt['is_negative']:
            text = f'''\
            У вас проверили работу "{lesson_title}".
            К сожалению, в работе нашлись ошибки.
            Ссылка: {lesson_url}'''
        else:
            text = f'''\
            У вас проверили работу "{lesson_title}"
            Преподавателю всё понравилось, можно приступать к следующему уроку!'''
        bot = telegram.Bot(token=telegram_token)
        bot.send_message(chat_id=tg_chat_id, text=textwrap.dedent(text))


if __name__ == '__main__':
    load_dotenv()
    dvmn_token = os.getenv('DVMN_TOKEN')
    dvmn_api_timeout = int(os.getenv('DVMN_API_TIMEOUT'))
    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
    tg_chat_id = os.getenv('TG_CHAT_ID')

    logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")
    logger.setLevel(logging.WARNING)
    logger.addHandler(LogsHandler(tg_chat_id, telegram_token))

    timestamp = get_last_timestamp(dvmn_token)
    logger.warning("Bot started...")
    while True:
        try:
            last_attempt = get_last_attempt(dvmn_token, dvmn_api_timeout, timestamp)
            if last_attempt['status'] == 'timeout':
                continue
            send_telegram_message(telegram_token, tg_chat_id, last_attempt)
            timestamp = last_attempt['last_attempt_timestamp']
        except requests.exceptions.ReadTimeout:
            dvmn_api_timeout += 10
            logging.warning(f"Looks like your timeout isn't big enough...\nNow it's {dvmn_api_timeout}...")
        except requests.exceptions.ConnectionError:
            logging.warning("It's seems you have some connection issues...\nTrying to reconnect...")
            time.sleep(10)
        except Exception as err:
            logger.error('Bot stopped working with an error...')
            logger.exception(err)

