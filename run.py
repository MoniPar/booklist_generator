import gspread 
from google.oauth2.service_account import Credentials

# Define the scope
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

# Add credentials to the account and authorise the client sheet
CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
# Get the spreadsheet
SHEET = GSPREAD_CLIENT.open("book_list")


def get_student_name():
    """
    Get student's first and last name from the user
    """
    print("Welcome to BookList Generator!\n")
    print("In order to run this program efficiently, "
          "please enter the correct student information "
          "when prompted and press the 'Enter' key.\n")
    print("When entering the student's first name, "
          "include their second name, if available. " 
          "Example: Mary Jane\n")
    name = input("Enter student's first name: \n")
    surname = input("Enter student's last name: \n")
    print(f"\nThank you! You are compiling a book list for {name} {surname}")
    

get_student_name()