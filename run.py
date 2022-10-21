# module re
import re
# module gspread
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
    Get student's first and last name from the user and converts the string
    values into a list of values.
    """
    print("Welcome to BookList Generator!\n")
    print("In order to run this program efficiently, please enter the correct "
          "student information when prompted and press the 'Enter' key.\n")
    print("When entering the student's full name, please start with the "
          "surname separated by a comma (,) from the name.  "
          "Example: Picard, Jean-Luc\n")

    name_str = input("Enter Student's Full Name: \n").title()
    if not re.search("^[a-zA-Z,.'\- ]+$", name_str):
        print("This is not a name!")
    else:
        print(f"\nThank you! You are compiling a book list for {name_str}")
    name_data = name_str.split(",")
    name_data = [i.strip() for i in name_data]
    
    validate_name(name_data)
 

def validate_name(values):
    """
    Inside the try, checks if there are 2 values with a minimum length of 3
    characters and raises ValueError if not.
    """
    print(values)
    try:
        if len(values) != 2:
            raise ValueError(
                f"Two values are required. You have entered {len(values)}"
            )
        if len(min(values)) <= 2:
            raise ValueError(
                "Input value must be longer than 2 characters. You have "
                f"entered {len(min(values))} characters for one or both "
                "of the values"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")

    

get_student_name()