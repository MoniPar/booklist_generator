import re
import sys
import gspread
import time
from google.oauth2.service_account import Credentials
from rich import print
from rich.console import Console
from os import system
# creates a console object
con = Console()

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


def clear():
    """"
    Clears the user terminal
    """
    system('clear')


def wait():
    """
    Delays text printing
    """
    time.sleep(1.75)


def wait_less():
    """"
    Delays text printing 
    """
    time.sleep(.75)


def wait_more():
    """
    Delays text printing more
    """
    time.sleep(2.5)


def get_student_name():
    """
    Gets student's first and last name from the user.
    Runs a while loop to collect a valid string of data from the user.
    The loop repeatedly requests data, until it is valid.
    """
    while True:
        con.print("\nWhen entering the student's full name, please start "
                  "with the surname separated by a comma (,) from the name. "
                  "[bright_magenta]Example: Picard, "
                  "Jean-Luc[/bright_magenta]\n", style="italic")
        name_str = input("Enter Student's Full Name: \n").title()
        con.print("\n[light_green]Validating your input...[/light_green]")

        if validate_name(name_str):
            print(f"\nThank you! You are compiling a booklist for {name_str}")
            break
    wait()
    return name_str


def validate_name(name_str):
    """
    Inside the try, checks for string values which meet the requirements for
    name values and raises TypeError if not.
    Converts the string values into a list of values.
    Checks for 2 values with a minimum length of 3 characters and raises
    ValueError if not.
    """
    student_ws = SHEET.worksheet("student_list").get_all_records()
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
        # if the values have already been written in the worksheet
        # https://stackoverflow.com/questions/24204087/how-to-get-multiple-dictionary-values
        for d in student_ws:
            if [d.get(k) for k in ['Surname', 'Name']] == name_data:
                print(f"\nLooks like {name_str} has already been "
                      "entered in the worksheet.")
                choice = input("\nWould you like to create a booklist "
                               f"for another {name_str}? (Y/N)\n").strip()
                if choice.capitalize() == 'Y':
                    return True
                elif choice.capitalize() == 'N':
                    return False
                else:
                    raise TypeError("Only Y or N is accepted. You have "
                                    f"entered '{choice}'")
    except TypeError as te:
        con.print(
            f"\nInvalid string: {te}, please try again.\n", style="bold red")
        wait()
        clear()
        return False
    except ValueError as e:
        con.print(
            f"\nInvalid data: {e}, please try again.\n", style="bold red")
        wait()
        clear()
        return False

    return True


def get_subjects():
    """
    Gets student's optional subjects from user.
    Runs a while loop to collect a valid string of data from the user.
    The loop repeatedly requests data until it is valid.
    Concatenates the 3 options into one string and returns the string.
    """
    clear()
    con.print("\nPlease choose 1 subject from each of the "
              "option lists below. You can enter the first "
              "three letters of the subject chosen "
              "[bright_magenta]Example: 'sci' for 'science' "
              "[/bright_magenta]\n", style="italic")

    while True:
        con.print("Option A: [bold]Science[/bold] or [bold]Music[/bold].")
        option_a = input("Enter subject here: \n").title()
        if validate_subjects(option_a, "Science, Music"):
            break
    while True:
        con.print("\nOption B: [bold]Business[/bold] or [bold]French[/bold].")
        option_b = input("Enter subject here: \n").title()
        if validate_subjects(option_b, "Business, French"):
            break
    while True:
        con.print("\nOption C: [bold]Engineering[/bold] or [bold]Art[/bold].")
        option_c = input("Enter subject here: \n").title()
        if validate_subjects(option_c, "Engineering, Art"):
            break

    print(f"\nYou have entered {option_a}, {option_b} "
          f"and {option_c}.\n")
    wait()
    clear()
    subjects_str = option_a + "," + option_b + "," + option_c

    return subjects_str


def validate_subjects(user_value, option_str):
    """
    Inside the try, checks for user input and raises a ValueError if option
    string does not contain the user input.
    """
    try:
        if not user_value:
            raise ValueError("No string found!")
        if len(user_value) <= 2:
            raise ValueError(
                "Input values must be longer than 2 characters")
        if user_value not in option_str:
            raise ValueError(f"{user_value} is not an option")
    except ValueError as e:
        con.print(
            f"Invalid data: {e}. Please try again.\n", style="bold red")
        wait()
        return False
    return True


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
    temp_data = entry + "," + names + "," + subjects + "," + "€" + totals
    temp_data = temp_data.split(",")
    student_data = [i.strip() for i in temp_data]

    return student_data


def books_total(subjects, names):
    """
    Checks if given optional subjects exist in worksheet.
    Prints out the relevant books for both optional and compulsory
    subjects. Works out the total price for the books.
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
                print("Retrieving Compulsory Subjects BookList for "
                      f"{names}\n")
                wait_less()
            # prints the values for compulsary subject, book and price
            con.print(f"[bright_cyan]{d['Subject']}:[/bright_cyan] "
                      f"[italic]{d['Book']}[/italic], "
                      f"[green]€{d['Price']}[/green]")
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
                              f"for {names}\n")
                        wait_less()
                    con.print(f"[bright_cyan]{d['Subject']}:[/bright_cyan] "
                              f"[italic]{d['Book']}[/italic], "
                              f"[green]€{d['Price']}[/green]")
                    wait_less()
                    totalcost += d['Price']
    # formats totalcost to 2 decimal places
    # adapted from https://pythonguides.com/python-print-2-decimal-places/
    format_totalcost = "{:.2f}".format(totalcost)
    con.print("\n[light_green]Calculating Total Cost of BookList..."
              "[/light_green]\n")
    wait_less()
    con.print(f"Total Cost of BookList: "
              f"[green]€{format_totalcost}[/green]\n")
    wait_less()
    return format_totalcost


def update_student_worksheet(student_data):
    """
    Updates student worksheet, adds new row with the list data provided.
    """
    con.print("[light_green]Updating student worksheet...[/light_green]\n")
    wait()
    student_ws = SHEET.worksheet("student_list")
    student_ws.append_row(student_data)
    print("Student worksheet updated successfully.\n")
    wait()
    menu()


def get_num_of_student_list():
    """"
    Gets the total number of students already added to the worksheet.
    """
    student_ws = SHEET.worksheet("student_list").get_all_values()
    student_num = (len(student_ws) - 1)
    print(f"\nThere are currently {student_num} students listed in "
          "the worksheet.\n")
    wait()
    menu()


def get_num_of_opt():
    """
    Gets the total number of each optional subject chosen.
    """
    print("\nFetching the number of students taking each option...\n")
    sdt_ws = SHEET.worksheet("student_list").get_all_records()

    science = sum(d.get('Option A') in 'Science' for d in sdt_ws)
    music = sum(d.get('Option A') in 'Music' for d in sdt_ws)
    business = sum(d.get('Option B') in 'Business' for d in sdt_ws)
    french = sum(d.get('Option B') in 'French' for d in sdt_ws)
    engineering = sum(d.get('Option C') in 'Engineering' for d in sdt_ws)
    art = sum(d.get('Option C') in 'Art' for d in sdt_ws)
    print(f"Science: {science}, Music: {music}")
    wait_less()
    print(f"Business: {business}, French: {french}")
    wait_less()
    print(f"Engineering: {engineering}, Art: {art}\n")
    wait_more()
    menu()


def print_last_entry():
    """
    Gets the student's name and optional subjects from the last
    row of the student worksheet and passes them into the
    books_total function
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


def menu():
    """
    Gives the user the option to select other features of the program.
    """
    print("-------------------------------")
    print("What would you like to do next?")
    print("-------------------------------")
    choice = input(" Add another student entry: 1\n "
                   "Get the number of students in the worksheet: 2\n "
                   "Get the number of options chosen: 3\n"
                   " Show me the last booklist again: 4\n"
                   " Exit program: X\n").strip()

    if choice == '1':
        clear()
        main()
    elif choice == '2':
        clear()
        get_num_of_student_list()
    elif choice == "3":
        clear()
        get_num_of_opt()
    elif choice == "4":
        print_last_entry()
    elif choice.capitalize() == "X":
        clear()
        # https://learnpython.com/blog/end-python-script/#:~:text=Ctrl%20%2B%20C%20on%20Windows%20can,ends%20and%20raises%20an%20exception.
        sys.exit("\nYou have chosen to exit BookList Generator. "
                 "GoodBye!")
    else:
        print(f"Invalid selection: {choice}, please try again.\n")
        wait()
        clear()
        menu()

    return True


def main():
    """
    Runs all program functions
    """
    wait()
    names = get_student_name()
    subjects = get_subjects()
    totals = books_total(subjects, names)
    entry = add_student_id()
    student_data = create_list(entry, names, subjects, totals)
    update_student_worksheet(student_data)


print("[bold yellow]Welcome to BookList Generator![/bold yellow]\n")
print("In order to run this program efficiently, "
      "please enter the correct information when "
      "prompted and press the 'Enter' key.\n")
main()