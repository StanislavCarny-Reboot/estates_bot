import requests
import re
import os
#from src.constants import (CHAT_ID,BOT_TOKEN)

CHAT_ID = os.getenv('CHAT_ID')
BOT_TOKEN = os.getenv('BOT_TOKEN')


def send_message(message_text):
    send_message_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    send_message_params = {"chat_id": CHAT_ID, "text": message_text}
    data = requests.get(send_message_url, params=send_message_params)
    return data

