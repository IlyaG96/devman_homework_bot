from dotenv import load_dotenv
import requests
import telegram
import os


def send_request_devman_ts(devman_token, payload):

    url = "https://dvmn.org/api/long_polling/"
    headers = {
        "Authorization": f"Token {devman_token}"
    }
    response = requests.get(url, headers=headers, params=payload)
    response.raise_for_status()

    return response.json()


def process_devman_response(response):

    lesson_title = response.get("new_attempts")[0].get("lesson_title")
    is_negative = response.get("new_attempts")[0].get("is_negative")
    lesson_url = response.get("new_attempts")[0].get("lesson_url")

    if is_negative:
        return f"Ваш урок '{lesson_title}' проверен. К сожалению, есть ошибки. \n" \
               f"Ссылка для перехода к уроку: {lesson_url}"
    return f"Ваш урок '{lesson_title}' проверен. Ошибок нет! Поздравляем! \n" \
           f"Ссылка для перехода к уроку: {lesson_url}"


def search_for_responses(devman_token, bot, chat_id):
    try:
        payload = None
        while True:
            response = send_request_devman_ts(devman_token, payload)
            timestamp = response.get("last_attempt_timestamp") or response.get("timestamp_to_request")
            payload = {"timestamp": timestamp}
            if not response.get("timestamp_to_request"):
                message = process_devman_response(response)
                bot.send_message(text=message, chat_id=chat_id)
                timestamp = response.get("timestamp_to_request")
                payload = {"timestamp": timestamp}

    except requests.exceptions.ReadTimeout:
        pass
    except requests.exceptions.ConnectionError:
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
