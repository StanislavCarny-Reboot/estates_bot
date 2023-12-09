

from pathlib import Path
import sys
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))
print(sys.path)

from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime
from src.constants import (SAMPLE_SPREADSHEET_ID,SCOPES,SERVICE_ACCOUNT_ENCODED)
from src.encoding import decode

SA_DECODED = decode(SERVICE_ACCOUNT_ENCODED)
creds = service_account.Credentials.from_service_account_info(SA_DECODED, scopes=SCOPES)
service = build('sheets','v4',credentials=creds)

def get_last_row_number():
  sheet = service.spreadsheets()
  result = sheet.values().get(spreadsheetId = SAMPLE_SPREADSHEET_ID,
                            range="Sheet1!A1:B1000").execute()
  num_rows = len(result['values'])
  return num_rows

def clear_sheet():
  sheet = service.spreadsheets()
  sheet.values().clear(spreadsheetId = SAMPLE_SPREADSHEET_ID,
                          range="Sheet1!A2:B1100").execute()


def create_timestamp():
  current_datetime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
  return current_datetime


def append_values_to_sheet(values):

  request = service.spreadsheets().values().append(
      spreadsheetId=SAMPLE_SPREADSHEET_ID,
      range="Sheet1",
      valueInputOption='USER_ENTERED',
      body={'values': values}
  )

  request.execute()


def log_new_hashes(new_hashes,clear_all=False):

  if clear_all==True:
    clear_sheet()
    print("Cleared all data")
    return


  row_number = get_last_row_number()
  if (row_number == 1000):
    clear_sheet()
    print("Cleared all data")

  timestamp = create_timestamp()
  new_data = [[timestamp,hash] for hash in new_hashes]

  append_values_to_sheet(new_data)
  print("New data appended")


  if __name__=="__main__":
    pass


