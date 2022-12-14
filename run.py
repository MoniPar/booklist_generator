"""
Imported libraries and modules for program support
"""
import re  # used in name validation
import sys   # used to provide a smooth exit from the program
import time  # used to add pauses when printing to the terminal
from os import system  # used to clear the terminal
import gspread  # used to interact with google sheets
from google.oauth2.service_account import Credentials
from rich import print  # used to add some styling to python print
from rich.console import Console  # used to add more styling for improved UX

# creates a console object
con = Console()

# Defines the scope
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

# Adds credentials to the account and authorises the client sheet
CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
# Gets the spreadsheet
SHEET = GSPREAD_CLIENT.open("book_list")


def clear():
    """"
    Clears the user terminal
    """
    system('clear')


def wait():
    """
    Delays text printing by 1750ms
    """
    time.sleep(1.75)


def wait_less():
    """"
    Delays text printing by 750ms
    """
    time.sleep(.75)


def wait_more():
    """
    Delays text printing by 3500ms
    """
    time.sleep(3.5)


# adapted from CI Love Sandwiches Walkthrough
def get_student_name():
    """
    Gets student's first and last name from the user.
    Runs a while loop to collect a valid string of data from the user.
    The loop repeatedly requests data, until it is valid.
    """
    while True:
        con.print("\n When entering the student's full name, please start "
                  "with\n the surname separated by a comma(,) from the name.\n"
                  " [yellow3]Example: Picard, "
                  "Jean-Luc[/yellow3]\n", style="italic")
        name_str = input("Enter Student's Full Name: \n").title()
        con.print("\n[light_green]Validating your input...[/light_green]")

        if validate_name(name_str):
            print(f"\nThank you! You are compiling a booklist for "
                  f"[cyan1]{name_str}[/cyan1]")
            break
    wait()
    return name_str


# adapted from CI Love Sandwiches Walkthrough
def validate_name(name_str):
    """
    Inside the try, checks for string values which meet the requirements for
    name values and raises TypeError if not.
    Converts the string values into a list of values.
    Checks for 2 values with a min length of 3 and a max length of 15
    characters and raises ValueError if not.
    """
    student_ws = SHEET.worksheet("student_list").get_all_records()
    try:
        # if user has not inserted an input
        if not name_str:
            raise TypeError("No string found!")
        # if input inserted has other characters other than alpha, comma(,),
        # period(.), apostrophe('), hyphen(-) or whitespace
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
        # if the length of each value is less than 3 characters
        if min(len(x) for x in name_data) <= 2:
            raise ValueError(
                "Input values must be longer than 2 characters")
        # if the length of each value is more than 15 characters
        if max(len(x) for x in name_data) >= 15:
            raise ValueError(
                "Input value must not be longer than 15 characters")
        # iterates through the dictionaries in the student worksheet list
        for d in student_ws:
            # if the user values equal the values of any dict's Surname and
            # Name keys
            # https://stackoverflow.com/questions/24204087/how-to-get-multiple-dictionary-values
            if [d.get(k) for k in ['Surname', 'Name']] == name_data:
                print(f"\nLooks like {name_str} has already been "
                      "entered in the worksheet.")
                choice = input("\nWould you like to create a booklist "
                               f"for another {name_str}? (Y/N)\n").strip()
                if choice.capitalize() == 'Y':
                    return True
                if choice.capitalize() == 'N':
                    return False
                raise TypeError("Only 'Y' or 'N' are accepted ")

    except TypeError as te:
        con.print(f"\nInvalid string: {te}, please enter the surname "
                  "and name again.\n", style="bold bright_red")
        wait_more()
        clear()
        return False
    except ValueError as e:
        con.print(f"\nInvalid data: {e}, "
                  "please try again.\n", style="bold bright_red")
        wait_more()
        clear()
        return False

    return True


def get_subjects():
    """
    Gets student's optional subjects from user.
    Runs 3 while loops to collect valid string of data for each of the
    three options from the user.
    The loops repeatedly request data until it is valid.
    Concatenates the 3 optional subjects into one string and returns the
    string.
    """
    clear()
    con.print("\n Please choose 1 subject from each of the "
              "option lists below.\n You can enter the first "
              "three letters of the subject chosen\n "
              "[yellow2]Example: 'sci' for 'science' "
              "[yellow2]\n", style="italic")

    while True:
        con.print(" Option A: [cyan1]Science[/cyan1] or [cyan1]Music[/cyan1].")
        option_a = input("Enter subject here: \n").title()
        # calls the validate function with the args for the first option
        if validate_subjects(option_a, "Science, Music"):
            # calls and assigns the returns of the helper function
            option_a = get_full_subject(option_a, "Science, Music")
            break
    while True:
        con.print(" \nOption B: [cyan1]Business[/cyan1] or "
                  "[cyan1]French[/cyan1].")
        option_b = input("Enter subject here: \n").title()
        if validate_subjects(option_b, "Business, French"):
            option_b = get_full_subject(option_b, "Business, French")
            break
    while True:
        con.print(" \nOption C: [cyan1]Engineering[/cyan1] or "
                  "[cyan1]Art[/cyan1].")
        option_c = input("Enter subject here: \n").title()
        if validate_subjects(option_c, "Engineering, Art"):
            option_c = get_full_subject(option_c, "Engineering, Art")
            break

    con.print(f"\nYou have entered [cyan1]{option_a}, {option_b}[/cyan1] "
              f"and [cyan1]{option_c}[/cyan1].\n")
    wait_more()
    clear()
    subjects_str = option_a + "," + option_b + "," + option_c

    return subjects_str


def validate_subjects(user_value, option_str):
    """
    Inside the try, checks for user input and raises a ValueError if user input
    is empty, smaller than 3 characters or is not part of the option string.
    """
    try:
        if not user_value:
            raise ValueError("No string found!")
        # if the length of the user input is less than 3 characters
        if len(user_value) <= 2:
            raise ValueError(
                "Input values must be longer than 2 letters")
        # if the user input is not one or part of the option string
        if user_value not in option_str:
            raise ValueError(f"{user_value} is not an option")

    except ValueError as e:
        con.print(
            f"Invalid data: {e}. Please type in one of the "
            "options listed.\n", style="bold bright_red")
        wait()
        return False

    return True


def get_full_subject(user_value, option_str):
    """
    Matches the user value with the first or second string in the option
    list and returns the full subject name for the options.
    """
    # splits the string into a list of strings
    option_list = option_str.split(", ")
    # assigns the first string to subject1
    subject1 = option_list[0]
    # assigns the second string to subject2
    subject2 = option_list[1]
    # if subject1 contains the user value
    if user_value in subject1:
        return subject1
    # if subject2 contains the user value
    if user_value in subject2:
        return subject2


def add_student_id():
    """
    Adds an id no. for each student's entry in the worksheet by
    iterating over the number of entries and adding 1 to each.
    """
    student_ws = SHEET.worksheet("student_list").get_all_values()
    num = 0
    for d in student_ws:
        num += 1
        entry = str(num)
    return entry


def create_list(entry, names, subjects, totals):
    """
    Creates a list with the names, optional subjects and total price.
    Returns the list created.
    """
    temp_data = entry + "," + names + "," + subjects + "," + "???" + totals
    temp_data = temp_data.split(",")
    student_data = [i.strip() for i in temp_data]

    return student_data


def books_total(subjects, names):
    """
    Matches the given optional subjects with those in the book worksheet.
    Prints out the relevant books for both optional and compulsory
    subjects. Adds up the book prices and prints the total cost
    to the terminal.
    """
    book_ws = SHEET.worksheet("book_list").get_all_records()
    # splits the subject string into a list
    values = subjects.split(",")
    comp_count = 0
    opt_count = 0
    totalcost = 0
    # iterates through the dicts in the book worksheet
    for d in book_ws:
        # if the value of Compulsory in the dict is equal to Y
        if d['Compulsory'] == 'Y':
            # starts count
            comp_count += 1
            # if count is equal to 1 prints "Retrieving..." statement
            if comp_count == 1:
                con.print("Retrieving Compulsory Subjects BookList for "
                          f"[cyan1]{names}[/cyan1]\n")
                wait_less()
            # prints the values for each compulsary subject, book and price
            con.print(f"    [yellow1]{d['Subject']}:[/yellow1] "
                      f"[italic]{d['Book']}[/italic], "
                      f"[green]???{d['Price']}[/green]")
            wait_less()
            # adds the values of Price
            totalcost += d['Price']
        else:
            # iterates through the list of values (user's subjects)
            for value in values:
                # if the value is equal to the value of Subject in the dict
                if value in d['Subject']:
                    opt_count += 1
                    if opt_count == 1:
                        print("\nRetrieving Optional Subjects BookList for "
                              f"for [cyan1]{names}[/cyan1]\n")
                        wait_less()
                    con.print(f"    [yellow1]{d['Subject']}:[/yellow1] "
                              f"[italic]{d['Book']}[/italic], "
                              f"[green]???{d['Price']}[/green]")
                    wait_less()
                    totalcost += d['Price']
    # formats totalcost to 2 decimal places
    # adapted from https://pythonguides.com/python-print-2-decimal-places/
    format_totalcost = "{:.2f}".format(totalcost)
    con.print("\n[light_green]Calculating Total Cost of BookList..."
              "[/light_green]\n")
    wait_less()
    con.print(f"    Total Cost of BookList: "
              f"[green]???{format_totalcost}[/green]\n")
    wait_less()
    return format_totalcost


def update_student_worksheet(student_data):
    """
    Updates student worksheet, adds new row with the list data provided.
    """
    con.print("Updating student worksheet...\n", style="light_green")
    wait_less()
    student_ws = SHEET.worksheet("student_list")
    student_ws.append_row(student_data)
    print("Student worksheet updated successfully.\n")
    wait_more()
    clear()
    menu()


def print_num_of_student_list():
    """"
    Gets the total number of students already added to the worksheet
    and prints it in the terminal.
    """
    student_ws = SHEET.worksheet("student_list").get_all_values()
    # gets the number of rows in the worksheet excluding the headings.
    student_num = (len(student_ws) - 1)
    con.print("\n Retrieving the current number of students in the "
              "worksheet...", style="light_green")
    wait()
    print(f"\n  There are currently {student_num} students listed in "
          "the worksheet.\n")
    wait()
    menu()


def print_num_of_opt():
    """
    Gets the total number of each optional subject chosen from the
    student worksheet and prints them in the terminal.
    """
    con.print("\n Retrieving the number of students taking each option...\n",
              style="light_green")
    wait()
    sdt_ws = SHEET.worksheet("student_list").get_all_records()
    # counts the total number of times each subject appears in the list
    # of dictionaries adapted from:
    # https://stackoverflow.com/questions/41658185/python-list-of-dictionaries-count-elements-based-on-key-of-dictionary
    science = sum(d.get('Option A') in 'Science' for d in sdt_ws)
    music = sum(d.get('Option A') in 'Music' for d in sdt_ws)
    business = sum(d.get('Option B') in 'Business' for d in sdt_ws)
    french = sum(d.get('Option B') in 'French' for d in sdt_ws)
    engineering = sum(d.get('Option C') in 'Engineering' for d in sdt_ws)
    art = sum(d.get('Option C') in 'Art' for d in sdt_ws)

    print(f"    Science: {science}, Music: {music}")
    wait_less()
    print(f"    Business: {business}, French: {french}")
    wait_less()
    print(f"    Engineering: {engineering}, Art: {art}\n")
    wait()
    menu()


def get_last_entry():
    """
    Gets the student's name and optional subjects from the last
    row of the student worksheet and passes them into the
    books_total function for printing
    """
    student_ws = SHEET.worksheet("student_list").get_all_values()
    last_value = student_ws[-1]
    surname = last_value[1]
    name = last_value[2]
    option_a = last_value[3]
    option_b = last_value[4]
    option_c = last_value[5]

    names = surname + ", " + name
    subjects = option_a + "," + option_b + "," + option_c

    books_total(subjects, names)
    menu()


def print_sdt_list():
    """
    Prints out the student worksheet in an easy to read format.
    """
    sdt_ws = SHEET.worksheet("student_list").get_all_records()
    con.print("\n Retrieving and formatting the entries from the student "
              "worksheet...\n", style="light_green")
    wait()
    for d in sdt_ws:
        con.print(f"{d['ID']}: [tan]{d['Surname']} {d['Name']}[/tan] - "
                  f"{d['Option A']}, {d['Option B']}, {d['Option C']}"
                  f" - [sea_green2]{d['Total Cost']}[/]\n")
        wait_less()
    wait_more()
    menu()


def menu():
    """
    Gives the user options to select other features of the program.
    Calls relevant functions according to user input.
    Prints error message if the user input is not one of the option numbers
    or letter X.
    """
    print("-------------------------------")
    print("What would you like to do next?")
    print("-------------------------------")
    wait_less()
    choice = input(" Add another student entry: 1\n "
                   "Get no. of students in worksheet: 2\n "
                   "Get no. of options chosen: 3\n"
                   " Print last booklist again: 4\n"
                   " Print student worksheet: 5\n"
                   " Exit program: X\n").strip()

    if choice == '1':
        # goes back to first function in main()
        clear()
        main()
    elif choice == '2':
        # goes to function to print no. of entries in worksheet
        clear()
        print_num_of_student_list()
    elif choice == "3":
        # goes to function to print the no. of each optional subject chosen
        clear()
        print_num_of_opt()
    elif choice == "4":
        # goes to helper function to get last entry and prints out booklist
        # through the books_total function
        clear()
        get_last_entry()
    elif choice == "5":
        # goes to function to print out student worksheet
        clear()
        print_sdt_list()
    elif choice.capitalize() == "X":
        clear()
        # https://learnpython.com/blog/end-python-script/#:~:text=Ctrl%20%2B%20C%20on%20Windows%20can,ends%20and%20raises%20an%20exception.
        sys.exit("\nYou have chosen to exit BookList Generator.\n "
                 "\n          Thank You and GoodBye!")
    else:
        con.print(f"Invalid selection: {choice} \nPlease choose "
                  "a number from the options above or 'X' "
                  "to exit.\n", style="bold bright_red")
        wait_more()
        clear()
        menu()

    return True


def main():
    """
    Runs main program functions
    """
    wait()
    names = get_student_name()
    subjects = get_subjects()
    totals = books_total(subjects, names)
    entry = add_student_id()
    student_data = create_list(entry, names, subjects, totals)
    update_student_worksheet(student_data)


print("---------------------------------------------------------\n")
print("             [bold yellow]Welcome to BookList Generator! "
      "[/bold yellow]\n")
print(" In order to run this program efficiently, please enter\n "
      " the correct information when prompted and press the\n "
      "                 'Enter' key.\n")
print("---------------------------------------------------------\n")
main()