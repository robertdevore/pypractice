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
regex_dict = {
    "Slack Token": r"(xox[pborsa]-[0-9]{12}-[0-9]{12}-[0-9]{12}-[a-z0-9]{32})",
    "RSA private key": r"-----BEGIN RSA PRIVATE KEY-----",
    "SSH (DSA) private key": r"-----BEGIN DSA PRIVATE KEY-----",
    "SSH (EC) private key": r"-----BEGIN EC PRIVATE KEY-----",
    "PGP private key block": r"-----BEGIN PGP PRIVATE KEY BLOCK-----",
    "AWS API Key": r"((?:A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16})",
    "Amazon MWS Auth Token": r"amzn\\.mws\\.[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
    "AWS API Key": r"AKIA[0-9A-Z]{16}",
    "AWS AppSync GraphQL Key": r"da2-[a-z0-9]{26}",
    "Facebook Access Token": r"EAACEdEose0cBA[0-9A-Za-z]+",
    "Facebook OAuth": r"[fF][aA][cC][eE][bB][oO][oO][kK].*['|\"][0-9a-f]{32}['|\"]",
    "GitHub": r"[gG][iI][tT][hH][uU][bB].*['|\"][0-9a-zA-Z]{35,40}['|\"]",
    "Generic API Key": r"[aA][pP][iI]_?[kK][eE][yY].*['|\"][0-9a-zA-Z]{32,45}['|\"]",
    "Generic Secret": r"[sS][eE][cC][rR][eE][tT].*['|\"][0-9a-zA-Z]{32,45}['|\"]",
    "Google API Key": r"AIza[0-9A-Za-z\\-_]{35}",
    "Google OAuth": r"[0-9]+-[0-9A-Za-z_]{32}\\.apps\\.googleusercontent\\.com",
    "Google (GCP) Service-account": r"\"type\": \"service_account\"",
    "Google OAuth Access Token": r"ya29\\.[0-9A-Za-z\\-_]+",
    "Heroku API Key": r"[hH][eE][rR][oO][kK][uU].*[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}",
    "MailChimp API Key": r"[0-9a-f]{32}-us[0-9]{1,2}",
    "Mailgun API Key": r"key-[0-9a-zA-Z]{32}",
    "Password in URL": r"[a-zA-Z]{3,10}://[^/\\s:@]{3,20}:[^/\\s:@]{3,20}@.{1,100}[\"'\\s]",
    "PayPal Braintree Access Token": r"access_token\\$production\\$[0-9a-z]{16}\\$[0-9a-f]{32}",
    "Picatic API Key": r"sk_live_[0-9a-z]{32}",
    "Slack Webhook": r"https://hooks\\.slack\\.com/services/T[a-zA-Z0-9_]{8}/B[a-zA-Z0-9_]{8}/[a-zA-Z0-9_]{24}",
    "Stripe API Key": r"sk_live_[0-9a-zA-Z]{24}",
    "Stripe Restricted API Key": r"rk_live_[0-9a-zA-Z]{24}",
    "Square Access Token": r"sq0atp-[0-9A-Za-z\\-_]{22}",
    "Square OAuth Secret": r"sq0csp-[0-9A-Za-z\\-_]{43}",
    "Telegram Bot API Key": r"[0-9]+:AA[0-9A-Za-z\\-_]{33}",
    "Twilio API Key": r"SK[0-9a-fA-F]{32}",
    "Twitter Access Token": r"[tT][wW][iI][tT][tT][eE][rR].*[1-9][0-9]+-[0-9a-zA-Z]{40}",
    "Twitter OAuth": r"[tT][wW][iI][tT][tT][eE][rR].*['|\"][0-9a-zA-Z]{35,44}['|\"]"
}

## Create the regex list.
regex_list = list(regex_dict.values())

# Open the CSV file in write mode.
file = open(csv_file, 'w', newline='')

# Create a CSV writer.
writer = csv.writer(file)

# Add a header row to the CSV file.
writer.writerow(['Found', 'Code', 'File', 'Line'])

# Define the directory to scan
directory = os.path.dirname(os.path.abspath(__file__))

# Counter.
counter = 0

# List of file extensions to scan
file_extensions = [".php", ".js", ".py", ".env", ".env.*", ".config", ".config.*", ".json", ".yaml", ".yml", ".ini", ".xml", ".txt"]

def scan_directory(directory, current_file_path):
    global counter
    # Use os.scandir() to loop through all the files in the directory
    with os.scandir(directory) as entries:
        for entry in entries:
            if entry.is_file() and entry.path != current_file_path and entry.name.endswith(tuple(file_extensions)):
                # Get the full path to the file.
                file_path = entry.path

                # Output line in terminal.
                print(f"Checking: {file_path}")

                # Open the file in read mode
                with open(file_path, "r", encoding='latin-1') as f:

                    # Use the enumerate() function to iterate over the lines in the file
                    for i, line in enumerate(f):

                        # List to store matching lines
                        matching_lines = []
                        google_api_key_found = False  # Track whether "Google API Key" has been found

                        # Iterate over the regex_list items.
                        for regex_key, regex_pattern in regex_dict.items():
                            # Search the string for a match to the regular expression
                            match = re.search(regex_pattern, line)

                            # Did we match?
                            if match:
                                # Check if it's a Google key
                                if "Google" in regex_key and not google_api_key_found:
                                    regex_key = "Google API Key"
                                    google_api_key_found = True

                                # Append the matching line to the list
                                matching_lines.append((regex_key, match.group(0)))

                        # If there are matching lines, write them as a single entry in the CSV file
                        if matching_lines:
                            # Combine the matching lines into a single string
                            combined_line = ', '.join([f"{regex_key}" for regex_key, matched_text in matching_lines])

                            # Save the file path, line number, code, and combined line to the CSV file.
                            writer.writerow([combined_line, line.strip()[:100], file_path, i + 1])
                            counter += 1
            elif entry.is_dir():
                # Recursively scan the subdirectory
                scan_directory(entry.path, current_file_path)

# Start scanning the directory
scan_directory(directory, os.path.abspath(__file__))

# Close the CSV file.
file.close()

end_time = time.time()

time_elapsed = end_time - start_time

print(f"Scan finished. Found {counter} errors and saved them to the {filename} file.")
print(f"Time elapsed: {time_elapsed:.2f} seconds")

