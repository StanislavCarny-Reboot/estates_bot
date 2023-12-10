import requests
import re
from src.constants import (BOT_TOKEN)



def get_estates(category_coding):
    all_apartments = []

    for cat,cat_index in category_coding.items():
        query_params = {'category_main_cb': ['1'],
            'category_sub_cb': [f'{cat_index}'],
            'category_type_cb': ['1'],
            'czk_price_summary_order2': ['0|8000000'],
            'estate_age': ['2'],
            'locality_region_id': ['10'],
            'per_page': ['999'],
            'tms': ['1701812490425']}

        r = requests.get("https://www.sreality.cz/api/cs/v2/estates", params=query_params)
        estates = r.json()['_embedded']['estates']
        base = f"https://www.sreality.cz/detail/prodej/byt/{cat}/"
        new_apartments = [(i['price'],i['locality'],f"{base}{i['seo']['locality']}/{i['hash_id']}") for i in estates]
        all_apartments = all_apartments + new_apartments
    return all_apartments


def get_latest_message_id():
    base_url = f'https://api.telegram.org/bot{BOT_TOKEN}/getUpdates' # ?offset=<{last_update_id-50}'
    r = requests.get(base_url)
    last_update_id = r.json()['result'][-1]['update_id'] -90
    return last_update_id


def get_chat_history(bot_token, chat_id,offset):
    base_url = f'https://api.telegram.org/bot{bot_token}/'
    params = {'CHAT_ID': chat_id,'offset':offset}
    response = requests.get(base_url + 'getUpdates', params=params)
    return response.json()

def get_hash_id(text):
  pattern = r'\b(\d+)\b'
  matches = re.findall(pattern, text)
  last_number = int(matches[-1]) if matches else None
  return last_number


def send_message(message_text,chat_id):
    send_message_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    send_message_params = {"chat_id": chat_id, "text": message_text}
    data = requests.get(send_message_url, params=send_message_params)
    return data



def pin_message(message_id,chat_id):
    pin_message_params = {
        "chat_id": chat_id,
        "message_id": message_id,
    }
    pin_message_url = f"https://api.telegram.org/bot{BOT_TOKEN}/pinChatMessage"
    data = requests.get(pin_message_url, params=pin_message_params)
    return data


def send_and_pin_chat_message(message,chat_id):
    response = send_message(message,chat_id)
    if response.status_code == 200:
        message_id = response.json()["result"]["message_id"]
        pin_response = pin_message(message_id,chat_id)
        print(f"Message {message_id} pinned successfully in chat")
    else:
        print(f"Error {response.status_code}")



def compare_hashes(old_hashes,new_hashes):
  old = set(old_hashes)
  new = set(new_hashes)
  new_estate_hashes = list(new-old)
  return new_estate_hashes



def send_new_estates(hashes_to_send,estates,chat_id):
  for i in estates:
    if get_hash_id(i[2]) in hashes_to_send:
      message = f"{i[1]} \n {i[2]}"
      send_and_pin_chat_message(message,chat_id)



def compare_hashes(old_hashes,new_hashes):
  old = set(old_hashes)
  new = set(new_hashes)
  new_estate_hashes = list(new-old)
  return new_estate_hashes



def send_new_estates(hashes_to_send,estates):
  for i in estates:
    if get_hash_id(i[2]) in hashes_to_send:
      message = f"{i[1]} \n {i[2]}"
      send_and_pin_chat_message(message)



def get_old_hashes(chat_history):
    hashes = []
    for i in chat_history['result']:
        try:
            message_text = i['message']['pinned_message']['text']
            hash = get_hash_id(message_text)
            hashes.append(hash)
        except KeyError:
            continue
    return hashes
