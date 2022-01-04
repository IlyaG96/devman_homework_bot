from dotenv import load_dotenv
from textwrap import dedent
import requests
import telegram
import time
import os

import logging
logging.basicConfig(level=logging.INFO)


def send_request_devman(devman_token, payload):
    url = "https://dvmn.org/api/long_polling/"
    headers = {
        "Authorization": f"Token {devman_token}"
    }
    response = requests.get(url, headers=headers, params=payload)
    response.raise_for_status()

    return response.json()


def process_devman_response(response):

    lesson_details = response.get("new_attempts")

    for attempt in lesson_details:
        lesson_title = attempt.get("lesson_title")
        is_negative = attempt.get("is_negative")
        lesson_url = attempt.get("lesson_url")

        if is_negative:
            return dedent(f"""
                        Ваш урок '{lesson_title}' проверен. К сожалению, есть ошибки.
                        Ссылка для перехода к уроку: {lesson_url}
                        """)
        return dedent(f"""
                    Ваш урок '{lesson_title}' проверен. Ошибок нет! Поздравляем!
                    Ссылка для перехода к уроку: {lesson_url}
                    """)


def search_for_responses(devman_token, bot, chat_id):

    payload = None
    while True:
        logging.info('Бот запущен')
        try:
            response = send_request_devman(devman_token, payload)
            timestamp = response.get("last_attempt_timestamp") or response.get("timestamp_to_request")
            payload = {"timestamp": timestamp}
            if not response.get("status") == "timeout":
                message = process_devman_response(response)
                bot.send_message(text=message, chat_id=chat_id)

        except requests.exceptions.ReadTimeout as read_timeout_ex:
            logging.warning(read_timeout_ex)
            time.sleep(30)
        except requests.exceptions.ConnectionError as conn_err_ex:
            logging.warning(conn_err_ex)
            time.sleep(60)
        logging.info("Ответ в течение 90 секунд не получен, перезапускаю бота")


def main():
    while True:
        load_dotenv()
        devman_token = os.getenv("DEVMAN_TOKEN")
        tg_token = os.getenv("TG_TOKEN")
        chat_id = os.getenv("CHAT_ID")
        bot = telegram.Bot(token=tg_token)
        try:
            search_for_responses(devman_token, bot, chat_id)
        except Exception as exception:
            exception_msg = exception.args[0]
            bot.send_message(text=exception_msg, chat_id=chat_id)
            time.sleep(60)


if __name__ == '__main__':
    main()
