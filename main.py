from datetime import datetime
from src.send_message import get_estates, get_hash_id, send_new_estates
from src.log_hash import (
    append_values_to_sheet,
    get_spreadsheet_data,
    compare_hashes,
    check_if_same_day,
    clear_sheet,
)
from src.constants import HISTORY_SPREADSHEET_ID
from src.constants import CHAT_ID, FORWARD_CHAT_ID
from loguru import logger


category_coding = {"2+kk": 4, "2+1": 5, "3+kk": 6, "3+1": 7}
estates = get_estates(category_coding)
new_hashes = [str(get_hash_id(i[2])) for i in estates]


history_data = get_spreadsheet_data(HISTORY_SPREADSHEET_ID)
old_hashes = [i[1] for i in history_data["values"][1:]]
new_data = compare_hashes(old_hashes, new_hashes)


if check_if_same_day(history_data):
    if new_data:
        append_values_to_sheet(new_data, HISTORY_SPREADSHEET_ID)
        logger.info("sending data to telegram")
        send_new_estates(new_data, estates, CHAT_ID)
        send_new_estates(new_data, estates, FORWARD_CHAT_ID)
        logger.success("all data sent")
    else:
        logger.info("No new data found")
else:

    logger.info("New day, clearing sheet")
    clear_sheet(HISTORY_SPREADSHEET_ID)
    append_values_to_sheet(new_data, HISTORY_SPREADSHEET_ID)
    send_new_estates(new_data, estates, CHAT_ID)
    send_new_estates(new_data, estates, FORWARD_CHAT_ID)
