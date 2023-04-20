import random
import string
import pyperclip
import datetime
import getpass
import hashlib


def generate_password(length=8, include_chars=None, exclude_chars=None):
    """Generate a random password of given length and specified characters."""
    # define character set based on user preferences
    characters = ''
    if include_chars:
        characters += include_chars
    else:
        characters = string.ascii_letters + string.digits + string.punctuation
    if exclude_chars:
        characters = ''.join(char for char in characters if char not in exclude_chars)

    # generate a random password
    password = ''.join(random.choice(characters) for i in range(length))

    return password


def calculate_strength(password):
    """Calculate the strength of the password."""
    score = 0
    if len(password) >= 8:
        score += 1
    if any(char.isupper() for char in password) and any(char.islower() for char in password):
        score += 1
    if any(char.isdigit() for char in password):
        score += 1
    if any(char in string.punctuation for char in password):
        score += 1

    # return a measure of strength based on the score
    if score == 0:
        return "Very weak"
    elif score == 1:
        return "Weak"
    elif score == 2:
        return "Medium"
    elif score == 3:
        return "Strong"
    elif score == 4:
        return "Very strong"


# prompt user to enter the desired length and character sets of the password
while True:
    try:
        length = int(input("Enter the desired length of your password: "))
        if length <= 0:
            print("Password length should be a positive integer.")
        else:
            break
    except ValueError:
        print("Invalid input. Please enter a positive integer.")

include_chars = input("Enter characters to include (press Enter for default): ")
exclude_chars = input("Enter characters to exclude (press Enter for none): ")

# generate a password and display it to the user
password = generate_password(length, include_chars, exclude_chars)
print("Your password is:", password)

# calculate and display the strength of the password
strength = calculate_strength(password)
print("Password strength:", strength)

# copy the password to the clipboard
pyperclip.copy(password)
print("Password copied to clipboard.")

# prompt user to save the password
while True:
    save_password = input("Do you want to save this password? (y/n) ")
    if save_password.lower() == 'y':
        # ask user for a name for the password
        password_name = input("Enter a name for this password: ")

        # ask user for the path to the password file
        password_file = input("Enter the path to the password file: ")

        # ask user for a master password to encrypt the password file
        master_password = getpass.getpass("Enter a master password to encrypt the password file: ")
        hash_master_password = hashlib.sha256(master_password.encode()).hexdigest()

        # write the password and its name to the password file
        with open(password_file, 'a') as f:
            f.write(f"{password_name}={password}|{strength}\n")

        # encrypt the password file with the master password
        with open(password_file, 'rb') as f:
            password_data = f.read()
        with open(password_file, 'wb') as f:
            f.write(hashlib.sha256(hash_master_password.encode()).digest())

# save the encrypted password data to a file with the current date and time
    # prompt user to save the password
    while True:
        save_password = input("Do you want to save this password? (y/n) ")
        if save_password.lower() == 'y':
            # ask user for a name for the password
            password_name = input("Enter a name for this password: ")

            # ask user for the path to the password file
            password_file = input("Enter the path to the password file: ")

            # ask user for a master password to encrypt the password file
            master_password = getpass.getpass("Enter a master password to encrypt the password file: ")
            hash_master_password = hashlib.sha256(master_password.encode()).hexdigest()

            # write the password and its name to the password file
            with open(password_file, 'a') as f:
                f.write(f"{password_name}={password}|{strength}\n")

            # encrypt the password file with the master password
            with open(password_file, 'rb') as f:
                password_data = f.read()
            with open(password_file, 'wb') as f:
                f.write(hashlib.sha256(hash_master_password.encode()).digest())

            # save the encrypted password data to a file with the current date and time
            now = datetime.datetime.now()
            filename = f"{now.strftime('%Y-%m-%d-%H-%M-%S')}.pwd"
            with open(filename, 'wb') as f:
                f.write(password_data)

            print("Password saved.")
            break
        elif save_password.lower() == 'n':
            break
        else:
            print("Invalid input. Please enter 'y' or 'n'.")
