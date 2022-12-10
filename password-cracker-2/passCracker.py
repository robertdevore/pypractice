import hashlib
import os
import time

# Get the current directory path.
directory = os.path.dirname(os.path.realpath(__file__))

# Define the hash to check against
hash_to_check = input("Enter your hash: ")

line_processed = 0

# Define the available hash algorithms
hash_algorithms = {
    "md5": hashlib.md5,
    "sha1": hashlib.sha1,
    "sha224": hashlib.sha224,
    "sha256": hashlib.sha256,
    "sha384": hashlib.sha384,
    "sha512": hashlib.sha512
}

# Prompt the user to select a hash algorithm
print("Select a hash algorithm:")
for i, algorithm in enumerate(hash_algorithms.keys()):
    print(f"{i+1}. {algorithm}")

# Read the user's selection
selection = input("Enter the number of the algorithm you want to use: ")

# Initialize a counter for the number of lines processed
lines_processed = 0

# Define a function that reads a text file and checks each password against the hash
def process_file(file_path):

    global lines_processed

    # Get the selected hash algorithm
    selected_algorithm = hash_algorithms[list(hash_algorithms.keys())[int(selection)-1]]

    # Open the file in read mode with the latin-1 encoding
    with open(file_path, "r", encoding="latin-1") as f:
        # Read the file lines
        file_lines = f.readlines()

        # Loop through the file lines
        for password in file_lines:
            # Hash the password using the selected algorithm
            password_hash = selected_algorithm(password.encode()).hexdigest()

            print(password)

            # Check if the password hash matches the hash to check
            if password_hash == hash_to_check:
                # Print a message if the password hash matches
                print(f"Found match for hash {hash_to_check} in file {file_path}: {password}")
                break

            # Increment the counter for the number of lines processed
            lines_processed += 1

        # Return the number of lines processed
        return lines_processed

if __name__ == '__main__':
    # Start the timer
    start = time.perf_counter()

    # Use os.walk() to loop through all the files in the directory
    # and all its subdirectories
    for root, dirs, files in os.walk(directory):
        # Loop through all the files
        for filename in files:
            # Check if the file is a text file
            if filename.endswith(".txt"):
                # Get the full path to the file
                file_path = os.path.join(root, filename)
                # Use the try and except statements to catch any errors that occur
                # during the execution of the script
                try:
                    # Apply the process_file() function to the file
                    lines_processed = process_file(file_path)
                except:
                    # Stop the timer
                    stop = time.perf_counter()

                    # Print a message with the time and number of lines processed
                    print(f"Process stopped early after {stop - start:0.4f} seconds and {lines_processed} lines processed")
                    break
            break
        break

    # Stop the timer
    stop = time.perf_counter()

    # Print the time it took to run the script
    print(f"Finished in {stop - start:0.4f} seconds")
    print(f"Processed {lines_processed} passwords. Found zero.")