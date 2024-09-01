from src.send_message import (
    get_estates,
    get_hash_id,
    get_latest_message_id,
    get_chat_history,
    get_old_hashes,
    send_new_estates,
    compare_hashes,
)

from src.constants import CHAT_ID, BOT_TOKEN, FORWARD_CHAT_ID
from src.log_hash import log_new_hashes

# from pathlib import Path
# import sys
# path_root = Path(__file__).parents[2]
# sys.path.append(str(path_root))
# print(sys.path)
category_coding = {"2+kk": 4, "2+1": 5, "3+kk": 6, "3+1": 7}


def main(send_all_estates=False):
    estates = get_estates(category_coding)
    new_hashes = [get_hash_id(i[2]) for i in estates]
    print("Estates downloaded")

    offset = get_latest_message_id()

    chat_history = get_chat_history(BOT_TOKEN, CHAT_ID, offset)

    old_hashes = get_old_hashes(chat_history)

    if send_all_estates:
        print("Sending all estates")
        send_new_estates(new_hashes, estates)
    else:
        hashes_to_send = compare_hashes(old_hashes, new_hashes)
        if len(hashes_to_send) == 0:
            print("No updates")
            return
        else:
            log_new_hashes(hashes_to_send, clear_all=True)
            print("Sending new estates")
            send_new_estates(hashes_to_send, estates, CHAT_ID)
            send_new_estates(hashes_to_send, estates, FORWARD_CHAT_ID)


if __name__ == "__main__":
    main()
