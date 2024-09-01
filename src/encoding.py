import json
import base64
import os


# from pathlib import Path
# import sys
# path_root = Path(__file__).parents[2]
# sys.path.append(str(path_root))
# print(sys.path)


# with open("key_file.json", 'r') as file:
#   json_data = json.load(file)


def encode(json_data):
    json_string = json.dumps(json_data)
    encoded_data_base64 = base64.b64encode(json_string.encode())
    return encoded_data_base64


def decode(encoded_data_base64):
    decoded_data = base64.b64decode(encoded_data_base64)
    decoded_json_data = json.loads(decoded_data.decode())
    return decoded_json_data
