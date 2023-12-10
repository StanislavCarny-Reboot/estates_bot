from dotenv import load_dotenv
import os
load_dotenv()



CHAT_ID = os.getenv('CHAT_ID')
BOT_TOKEN = os.getenv('BOT_TOKEN')
BASE_URL = f'https://api.telegram.org/bot{BOT_TOKEN}/'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SAMPLE_SPREADSHEET_ID = "1irbsoEGU0UEBAVIEbGgtyR4vRGJlgWnnDaQJq1XLiIM"
SERVICE_ACCOUNT_ENCODED = os.getenv('SERVICE_ACCOUNT_ENCODED')
FORWARD_CHAT_ID = os.getenv('FORWARD_CHAT_ID')



if __name__=="__main__":
    pass

