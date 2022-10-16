#23456789 123456789 123456789 1233456789 123456789 123456789 123456789 1234567890
import gspread 
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("book_list")

price_list = SHEET.worksheet("subject-book-price_list")

data = price_list.get_all_values()

print(data)