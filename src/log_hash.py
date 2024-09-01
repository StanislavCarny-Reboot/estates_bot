# from pathlib import Path
# import sys
# path_root = Path(__file__).parents[2]
# sys.path.append(str(path_root))
# print(sys.path)

from loguru import logger
from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime
from src.constants import (
    SAMPLE_SPREADSHEET_ID,
    HISTORY_SPREADSHEET_ID,
    SCOPES,
    SERVICE_ACCOUNT_ENCODED,
)
from src.encoding import decode


SA_DECODED = decode(SERVICE_ACCOUNT_ENCODED)
creds = service_account.Credentials.from_service_account_info(SA_DECODED, scopes=SCOPES)
service = build("sheets", "v4", credentials=creds)


def get_last_row_number(spreadsheet_id):
    sheet = service.spreadsheets()
    result = (
        sheet.values()
        .get(spreadsheetId=spreadsheet_id, range="Sheet1!A1:B1000")
        .execute()
    )
    num_rows = len(result["values"])
    return num_rows


def clear_sheet(spreadsheet_id):
    sheet = service.spreadsheets()
    sheet.values().clear(
        spreadsheetId=spreadsheet_id, range="Sheet1!A2:B1100"
    ).execute()


def append_values_to_sheet(values, spreadsheet_id):

    timestamp = datetime.today().strftime("%Y-%m-%d")
    new_data = [[timestamp, hash] for hash in values]

    request = (
        service.spreadsheets()
        .values()
        .append(
            spreadsheetId=spreadsheet_id,
            range="Sheet1",
            valueInputOption="USER_ENTERED",
            body={"values": new_data},
        )
    )

    request.execute()
    logger.success(f"New data appended: {new_data}")


def compare_hashes(old_hashes, new_hashes):
    old = set(old_hashes)
    new = set(new_hashes)
    new_estate_hashes = list(new - old)
    return new_estate_hashes


def check_if_same_day(history_data):
    current_date = datetime.today().strftime("%Y-%m-%d")

    if not history_data:
        max_date_history = datetime.today().strftime("%Y-%m-%d")
    else:
        max_date_history = max([i[0] for i in history_data["values"][1:]])
    return current_date == max_date_history


def get_spreadsheet_data(spreadsheet_id):
    sheet = service.spreadsheets()
    result = (
        sheet.values()
        .get(spreadsheetId=spreadsheet_id, range="Sheet1!A1:B1000")
        .execute()
    )
    return result
