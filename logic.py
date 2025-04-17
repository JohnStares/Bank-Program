import random

def generate_acct_no():
    act_no = ""
    for _ in range(6):
        act_no += str(random.choice(range(0, 9)))
    return act_no

def validate_name(x):
    numbers = "1,2,3,4,5,6,7,8,9,0"
    symbols = "!@#$%^&*()}{[]?/>.<,`~|"";:=+_"
    if x.isdigit():
        print("Name cannot be numbers. Please input a valid name and try again.")
    elif len(x) <= 2:
        print("Name is too short.")
    elif any(num in numbers for num in x):
        print("Name shouldn't have a number in it. Please input a valid name and try again.")
    elif any(sym in symbols for sym in x):
        print("There shouldn't be symbol(s) in name. Please input a valid name and try again.")
    else:
        return x.capitalize()

def validate_input(x):
    symbols = "!@#$%^&*()}{[]?/>.<,`~|"";:=+_"
    if any(char.isalpha() for char in x):
        print("Account number doesn't have alphabets. Please, input a valid account number and try again.")
    elif any(sym in symbols for sym in x):
        print("Account number doesn't have symbols. Please, input a valid account number and try again.")
    elif len(x) < 6 or len(x) > 6:
        print("Account number has an invalid length. Required length is 6")
    else:
        return x

def validate_amount(x):
    symbols = "!@#$%^&*()}{[]?/>.<,`~|"";:=+_"
    if any(dig.isalpha() for dig in x):
        print("Please, input a valid amount and try again. No alphabets")
    elif x is None:
        print("Amount can't be empty.")
    elif any(sym in symbols for sym in x):
        print("Invalid amount input. No symbols.")
    else:
        return float(x)
