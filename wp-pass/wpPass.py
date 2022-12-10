import bcrypt
import threading
import os
import argparse

# Use the argparse module to parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('wp_password_hash', help='the WordPress password hash to check against')
parser.add_argument('input_file', help='the file containing the passwords to check')
args = parser.parse_args()

# Lock to protect shared state
lock = threading.Lock()

# Flag to indicate that a password has been found
found = False

def check_password(password: str) -> None:
    """
    Check a password against the WordPress password hash.

    :param password: The password to check.
    """
    global found
    global lock

    # Hash the password using the bcrypt algorithm
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    # Convert the password hash to a string and compare it to the WordPress password hash
    if password_hash.decode() == args.wp_password_hash:
        # The password matches the WordPress password hash
        print(f'The password "{password}" matches the WordPress password hash.')

        # Set the flag to indicate that the password has been found
        with lock:
            found = True


# Open the file containing the passwords
input_file = os.path.join(os.getcwd(), args.input_file)
with open(input_file, 'r') as f:
    # Read each line (password) from the file
    for line in f:
        # Strip leading and trailing whitespace from the password
        password = line.strip()

        # Create a thread to check the password
        thread = threading.Thread(target=check_password, args=(password,))

        # Start the thread
        thread.start()

    # Wait for all threads to finish
    while threading.active_count() > 1:
        pass

    # Check if the password was found
    if not found:
        # The password was not found in the list
        print('The password was not found in the list.')