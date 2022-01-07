from dotenv import load_dotenv
from textwrap import dedent
import requests
import telegram
import time
import os
import logging


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


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


def search_for_responses(devman_token, bot, chat_id, logger):

    payload = None
    while True:
        try:
            response = send_request_devman(devman_token, payload)
            timestamp = response.get("last_attempt_timestamp") or response.get("timestamp_to_request")
            payload = {"timestamp": timestamp}
            if not response.get("status") == "timeout":
                message = process_devman_response(response)
                bot.send_message(text=message, chat_id=chat_id)

        except requests.exceptions.ConnectionError as conn_err_ex:
            logger.warning(conn_err_ex)
            time.sleep(120)
        except Exception as exception:
            logger.error(exception, exc_info=True)
            time.sleep(120)


def main():

    load_dotenv()
    devman_token = os.getenv("DEVMAN_TOKEN")
    tg_token = os.getenv("TG_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    logger = logging.getLogger('Logger')
    logger.setLevel(logging.WARNING)
    bot = telegram.Bot(token=tg_token)
    logger.addHandler(TelegramLogsHandler(bot, chat_id))
    search_for_responses(devman_token, bot, chat_id, logger)


if __name__ == '__main__':
    main()
