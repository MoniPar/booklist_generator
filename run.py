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
    Gets student's first and last name from the user.
    Runs a while loop to collect a valid string of data from the user. 
    The loop repeatedly requests data, until it is valid.
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
        print("\nValidating your input...")

        if validate_name(name_str):
            print(f"Thank you! You are compiling a booklist for {name_str}.\n")
            break
    
    return name_str
 

def validate_name(name_str):
    """
    Inside the try, checks for string values which meet the requirements for
    name values and raises TypeError if not.
    Converts the string values into a list of values.
    Checks for 2 values with a minimum length of 3 characters and raises
    ValueError if not.
    """
    try:
        if not name_str:
            raise TypeError("No string found!")
        if not re.search(r"^[a-zA-Z,.'\- ]+$", name_str):
            raise TypeError(f"{name_str} is not a name")
        # splits a string at the commas, into a list
        name_data = name_str.split(",")
        # strips any leading or trailing spaces from the string
        name_data = [i.strip() for i in name_data]
        if len(name_data) != 2:
            raise ValueError(
                f"Two values are required. You have entered {len(name_data)}"
            )
        if min(len(x) for x in name_data) <= 2:
            raise ValueError(
                "Input values must be longer than 2 characters")
    except TypeError as te:
        print(f"Invalid string: {te}, please try again.\n")
        return False
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True


def get_subjects():
    """
    Gets student's optional subjects from user.
    Runs a while loop to collect a valid string of data from the user.
    Concatenates the 3 options into one string and returns the string.
    """
    while True:
        print("Please choose 1 subject from the option lists below.\n")
        print("Option A: Science or Music.")
        option_a = input("Enter subject here: \n").title()
        print("\nOption B: Business or French.")
        option_b = input("Enter subject here: \n").title()
        print("\nOption C: Engineering or Art.")
        option_c = input("Enter subject here: \n").title()
        
        print(f"\nYou have entered {option_a}, {option_b} and {option_c}.")

        subjects_str = option_a + "," + option_b + "," + option_c
        break

    return subjects_str


def create_list(names, subjects):
    """
    Creates a list with the names and the subjects and returns the list.
    """
    temp_data = names + "," + subjects
    temp_data = temp_data.split(",")
    student_data = [i.strip() for i in temp_data]

    return student_data


def update_student_worksheet(student_data):
    """
    Updates student worksheet, adds new row with the list data provided.
    """
    print("Updating student worksheet...\n")
    student_worksheet = SHEET.worksheet("student_list")
    student_worksheet.append_row(student_data)
    print("Student worksheet updated successfully.\n")


names = get_student_name()
subjects = get_subjects()
student_data = create_list(names, subjects)
update_student_worksheet(student_data)