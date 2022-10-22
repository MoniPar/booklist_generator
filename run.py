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
    values into a list of values. Run a while loop to collect a valid string
    of data from the user.  The loop will repeatedly request data, until it
    is valid.
    """
    while True:
        print("Welcome to BookList Generator!\n")
        print("In order to run this program efficiently, please enter "
              "the correct student information when prompted and "
              "press the 'Enter' key.\n")
        print("When entering the student's full name, please start "
              "with the surname separated by a comma (,) from the name. "
              "Example: Picard, Jean-Luc\n")

        name_str = input("Enter Student's Full Name: \n").title()
        
        name_data = name_str.split(",")
        name_data = [i.strip() for i in name_data]

        if validate_name(name_str, name_data):
            print(f"Thank you! You are compiling a booklist for {name_str}.")
            break
    
    return name_data
 

def validate_name(name_str, name_data):
    """
    Inside the try, checks for string values which meet the requirements for
    name values and raises TypeError if not. It also checks if there are 2
    values with a minimum length of 3 characters and raises ValueError if not.
    """
    try:
        if not name_str:
            raise TypeError("No string found!")
        if not re.search("^[a-zA-Z,.'\- ]+$", name_str):
            raise TypeError(f"{name_str} is not a name")
        if len(name_data) != 2:
            raise ValueError(
                f"Two values are required. You have entered {len(name_data)}"
            )
        if min(len(x) for x in name_data) <= 2:
            raise ValueError(
                "Input values must be longer than 2 letters")
    except TypeError as te:
        print(f"Invalid string: {te}, please try again.\n")
        return False
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True


def update_student_worksheet(names):
    """
    Update student worksheet, add new row with the list data provided.
    """
    print("Updating sales worksheet...\n")
    student_worksheet = SHEET.worksheet("student_list")
    student_worksheet.append_row(names)
    print("Student worksheet updated successfully.\n")


names = get_student_name()
name_data = [str(name) for name in names]
update_student_worksheet(name_data)