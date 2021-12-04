import os
import requests
from dotenv import load_dotenv


def main():
    load_dotenv()
    devman_token = os.getenv("DEVMAN_TOKEN")
