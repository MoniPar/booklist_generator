# module re
import re
# module gspread
import gspread
from google.oauth2.service_account import Credentials

# Defines the scope
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

# Adds credentials to the account and authorise the client sheet
CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
# Gets the spreadsheet
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


def books_total(subjects):
    """
    Checks if given optional subjects exist in worksheet.
    Prints out the relevant books and prices for both optional and compulsory
    subjects. Works out the total price for the books.
    """
    book_price = SHEET.worksheet("subject-book-price_list").get_all_records()
    comp_prices = []
    comp_total = 0
    opt_prices = []
    opt_total = 0
    total_price = []
    total_cost = 0
    # splits the subjects string into a list
    values = subjects.split(",")
    print("Retrieving Optional Subjects BookList...\n")
    # iterates through the list of dictionaries
    for d in book_price:
        # iterates through the list of subjects
        for value in values:
            # if a value in the list exists as a value for the Subject key
            if value in d['Subject']:
                opt_prices.append(d['Price'])
                print(f"{d['Subject']}: {d['Book']}, {d['Price']}")
                break
    # gets the sum of opt_prices
    opt_total = sum(opt_prices)
    # formats it to 2 decimal places
    # taken from https://pythonguides.com/python-print-2-decimal-places/
    format_opt_total = "{:.2f}".format(opt_total)
    print(f"Total Price: €{format_opt_total}\n")

    print("Retrieving Compulsory Subjects BookList...\n")
    # iterates through the index of the list of dictionaries
    for i in range(len(book_price)):
        # if the values of 'Compulsory' are equal to 'Y'
        if book_price[i]['Compulsory'] == 'Y':
            comp_prices.append(book_price[i]['Price'])
            print(f"{book_price[i]['Subject']}: {book_price[i]['Book']}, "
                  f" €{book_price[i]['Price']}")

    comp_total = sum(comp_prices)
    format_comp_total = "{:.2f}".format(comp_total)
    print(f"Total Price: €{format_comp_total}\n")

    print("Calculating Total Cost of BookList...\n")
    total_price.append(opt_total)
    total_price.append(comp_total)
    total_cost = sum(total_price)
    format_total_cost = "{:.2f}".format(total_cost)
    print(f"Total Cost of BookList: €{format_total_cost}\n")


names = get_student_name()
subjects = get_subjects()
student_data = create_list(names, subjects)
update_student_worksheet(student_data)
books_total(subjects)