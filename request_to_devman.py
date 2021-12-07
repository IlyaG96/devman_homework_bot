from dotenv import load_dotenv
from textwrap import dedent
import requests
import telegram
import time
import os


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

    for num, new_attempts in enumerate(lesson_details):
        lesson_title = new_attempts.get("lesson_title")
        is_negative = new_attempts.get("is_negative")
        lesson_url = new_attempts.get("lesson_url")

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

    try:
        payload = None
        while True:
            response = send_request_devman(devman_token, payload)
            timestamp = response.get("last_attempt_timestamp") or response.get("timestamp_to_request")
            payload = {"timestamp": timestamp}
            if not response.get("status") == "timeout":
                message = process_devman_response(response)
                bot.send_message(text=message, chat_id=chat_id)

    except requests.exceptions.ReadTimeout:
        pass
    except requests.exceptions.ConnectionError:
        time.sleep(60)
        pass


def main():

    load_dotenv()
    devman_token = os.getenv("DEVMAN_TOKEN")
    tg_token = os.getenv("TG_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    bot = telegram.Bot(token=tg_token)
    while True:
        search_for_responses(devman_token, bot, chat_id)


if __name__ == '__main__':
    main()
