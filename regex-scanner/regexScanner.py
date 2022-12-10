import os
import csv
import re
import time

# Get the script start time.
start_time = time.time()

# Get current time.
timestr = time.strftime("%Y%m%d-%H%M%S")

# Set the path to the WordPress root directory.
path = os.path.dirname(__file__)
# Generate the CSV file name.
filename = 'regex-scan-results-' + timestr + '.csv'
# Set the name of the CSV file.
csv_file = os.path.join(path, filename)

# List of regex to use.
regex_list = [
    r"^\$[a-zA-Z0-9]*\{([a-zA-Z0-9])\}",
    r"\bcreate_function\(.*\)",
    r"\beval\(.*\)",
    r"\bassert\(.*\)",
    r"\bfopen\(.*\)",
    r"\btmpfile\(.*\)",
    r"\bbzopen\(.*\)",
    r"\bgzopen\(.*\)",
    r"\bchgrp\(.*\)",
    r"\bchmod\(.*\)",
    r"\bchown\(.*\)",
    r"\bcopy\(.*\)",
    r"\bfile_put_contents\(.*\)",
    r"\blchgrp\(.*\)",
    r"\blchown\(.*\)",
    r"\blink\(.*\)",
    r"\bmkdir\(.*\)",
    r"\bmove_uploaded_file\(.*\)",
    r"\brename\(.*\)",
    r"\brmdir\(.*\)",
    r"\bsymlink\(.*\)",
    r"\btempnam\(.*\)",
    r"\btouch\(.*\)",
    r"\bunlink\(.*\)",
    r"\bftp_get\(.*\)",
    r"\bftp_nb_get\(.*\)",
    r"\bfile_get_contents\(.*\)",
    r"\bfile\(.*\)",
    r"\bfile_exists\(.*\)",
    r"\bfileatime\(.*\)",
    r"\bfilectime\(.*\)",
    r"\bfilegroup\(.*\)",
    r"\bglob\(.*\)",
    r"\bis_executable\(.*\)",
    r"\bgzfile\(.*\)",
    r"\brealpath\(.*\)",
    r"\bftp_put\(.*\)",
    r"\bhash_file\(.*\)",
    r"\bphpinfo\(.*\)",
    r"\bget_current_user\(.*\)",
    r"\bgetmypid\(.*\)",
    r"\bgetmyuid\(.*\)",
    r"\bextract\(.*\)",
]

## Evil regex.
evil_regex = ["(a+)+", "([a-zA-Z]+)*", "(a|aa)+", "(a|a?)+", r"(.*a){x} for x \> 10"]

# Open the CSV file in write mode.
file = open(csv_file, 'w', newline='')

# Create a CSV writer.
writer = csv.writer(file)

# Add a header row to the CSV file.
writer.writerow(['File', 'Line', 'Code', 'Error'])

# Define the directory to scan
directory = "."

# Counter.
counter = 0

def scan_directory(directory):
    global counter
    # Use os.scandir() to loop through all the files in the directory
    with os.scandir(directory) as entries:
        for entry in entries:
            if entry.is_file() and entry.name.endswith(".php"):
                # Get the full path to the file.
                file_path = entry.path

                # Get the full path to the directory.
                #file_dir = os.path.dirname(file_path)

                # Output line in terminal.
                print(f"Checking: {file_path}")

                # Open the file in read mode
                with open(file_path, "r", encoding='latin-1') as f:

                    # Use the enumerate() function to iterate over the lines in the file
                    for i, line in enumerate(f):

                        # Iterate over the substrings in the list
                        for substring in evil_regex:

                            # Check if the substring is in the line of text
                            if substring in line:

                                # Save the file path, line number, code, and error message to the CSV file.
                                writer.writerow([file_path, i + 1, line.strip(), substring])
                                counter += 1

                        # Iterate over the regex_list items.
                        for regex_item in regex_list:
                            # Search the string for a match to the regular expression
                            match = re.search(regex_item, line)

                            # Did we match?
                            if match:
                                # Save the file path, line number, code, and error message to the CSV file.
                                writer.writerow([file_path, i + 1, line.strip(), match.group(0)])
                                counter += 1
            elif entry.is_dir():
                # Recursively scan the subdirectory
                scan_directory(entry.path)

# Start scanning the directory
scan_directory(directory)

# Close the CSV file.
file.close()

end_time = time.time()

time_elapsed = end_time - start_time

print(f"Scan finished. Found {counter} errors and saved them to the {filename} file.")
print(f"Time elapsed: {time_elapsed:.2f} seconds")
