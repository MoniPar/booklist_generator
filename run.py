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
            print(f"\nThank you! You are compiling a booklist for {name_str}.")
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
        # if user has not inserted an input 
        if not name_str:
            raise TypeError("No string found!")
        # if input inserted has other characters other than alpha, comma(,),
        # period(.), apostrophe(') or hyphen(-) 
        if not re.search(r"^[a-zA-Z,.'\- ]+$", name_str):
            raise TypeError(f"{name_str} is not a name")
        # splits a string at the commas, into a list of strings
        name_data = name_str.split(",")
        # strips any leading or trailing spaces from the strings
        name_data = [i.strip() for i in name_data]
        # if the list does not contain 2 values
        if len(name_data) != 2:
            raise ValueError(
                f"Two values are required. You have entered {len(name_data)}"
            )
        # if the length of the values is less than 3 characters
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
    The loop repeatedly requests data until it is valid.
    Concatenates the 3 options into one string and returns the string.
    """
    while True:
        print("\nPlease choose 1 subject from each of the "
              "option lists below.\n")
        print("Option A: Science or Music.")
        option_a = input("Enter subject here: \n").title()
        if validate_subjects(option_a, "Science, Music"):
            print("\nOption B: Business or French.")
            option_b = input("Enter subject here: \n").title()
            if validate_subjects(option_b, "Business, French"):
                print("\nOption C: Engineering or Art.")
                option_c = input("Enter subject here: \n").title()
                if validate_subjects(option_c, "Engineering, Art"):
                    print(f"\nYou have entered {option_a}, {option_b} "
                          f"and {option_c}.\n")

                    subjects_str = option_a + "," + option_b + "," + option_c
                    break

    return subjects_str


def validate_subjects(user_value, option_str):
    """
    Inside the try, checks for user input and raises a ValueError if option
    string does not contain the user input.
    """
    try:
        if not user_value:
            raise ValueError("No string found!")
        # .__contains__ is an instance method which checks whether the string 
        # object contains the specified string object and returns a boolean. 
        # https://www.digitalocean.com/community/tutorials/python-string-contains
        if not option_str.__contains__(user_value):
            raise ValueError(f"{user_value} is not an option!")
    except ValueError as e:
        print(f"Invalid string: {e}, please try again.\n")
        return False

    return True


def create_list(names, subjects, totals):
    """
    Creates a list with the names, optional subjects and total price.
    Returns the list created.
    """
    temp_data = names + "," + subjects + "," + "€" + totals
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
    Prints out the relevant books for both optional and compulsory
    subjects. Works out the total price for the books.
    """
    book_list = SHEET.worksheet("book_list").get_all_records()
    # splits the subject string into a list
    values = subjects.split(",")
    comp_count = 0
    opt_count = 0
    totalcost = 0
    # iterates through the dicts in the book list
    for d in book_list:
        # if the value of Compulsory in the dict is equal to Y
        if d['Compulsory'] == 'Y':
            # starts count
            comp_count += 1
            # if count is equal to 1 prints "Retrieving..." statement
            if comp_count == 1:
                print("Retrieving Compulsory Subjects BookList...\n")
            # prints each dict's Subject's, Book's, Price's value
            print(f"{d['Subject']}: {d['Book']}, "
                  f"€{d['Price']}")
            # adds the values of Price
            totalcost += d['Price']
        else:
            # iterates through the list of values (user's subjects)
            for value in values:
                # if the value is equal to the value of Subject in the dict
                if value in d['Subject']:
                    opt_count += 1
                    if opt_count == 1:
                        print("\nRetrieving Optional Subjects BookList...\n")
                    print(f"{d['Subject']}: {d['Book']}, "
                          f"€{d['Price']}")
                    totalcost += d['Price']
    # formats totalcost to 2 decimal places
    # adapted from https://pythonguides.com/python-print-2-decimal-places/
    format_totalcost = "{:.2f}".format(totalcost)
    print("\nCalculating Total Cost of BookList...\n")
    print(f"Total Cost of BookList: €{format_totalcost}\n")

    return format_totalcost


def main():
    """
    Runs all program functions
    """
    names = get_student_name()
    subjects = get_subjects()
    totals = books_total(subjects)
    student_data = create_list(names, subjects, totals)
    update_student_worksheet(student_data)


main()