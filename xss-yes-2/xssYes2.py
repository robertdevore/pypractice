import sys
import requests
from bs4 import BeautifulSoup
import re
import time
from tqdm import tqdm
from datetime import datetime

def scan_for_xss(target_url, wordlist_file):
    # Load the wordlist from file
    with open(wordlist_file, 'r') as file:
        wordlist = file.read().splitlines()

    # Send a GET request to the target URL
    response = requests.get(target_url)

    # Parse the response HTML using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all input fields in the HTML form
    input_fields = soup.find_all('input') + soup.find_all('textarea')

    # Define a regular expression pattern to match XSS payloads
    xss_pattern = re.compile(r'<script>.+</script>')

    # Track the vulnerabilities found
    vulnerabilities = []

    # Initialize the progress bar
    progress_bar = tqdm(total=len(wordlist) * len(input_fields), unit='scan')

    # Check each input field for potential XSS vulnerabilities
    for input_field in input_fields:
        # Check if the input field accepts user input
        input_types = ['text', 'textarea', 'submit', 'password', 'phone']  # Add more types as needed
        if input_field.get('type') in input_types:
            input_id = input_field.get('id')
            input_name = input_field.get('name')

            # Test each payload from the wordlist against the input field
            for xss_payload in wordlist:
                # Replace the input field value with the XSS payload
                input_field['value'] = xss_payload

                # Submit the form with the modified payload
                form_data = soup.find('form').find_all('input')
                payload = {input.get('name'): input.get('value') for input in form_data}
                response = requests.post(target_url, data=payload)

                # Check if the XSS payload is reflected in the response
                if xss_pattern.search(response.text):
                    vulnerability = {
                        'URL': target_url,
                        'XSS Script': xss_payload,
                        'Input ID': input_id,
                        'Input Name': input_name
                    }
                    vulnerabilities.append(vulnerability)

                # Update the progress bar
                progress_bar.update()

    # Close the progress bar
    progress_bar.close()

    # Save the vulnerabilities to a file
    save_vulnerabilities(target_url, vulnerabilities)

def save_vulnerabilities(target_url, vulnerabilities):
    # Generate the filename
    current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'{target_url}_xss_vulnerabilities_{current_time}.txt'

    # Save the vulnerabilities to the file
    with open(filename, 'w') as file:
        for vulnerability in vulnerabilities:
            file.write('URL: ' + vulnerability['URL'] + '\n')
            file.write('XSS Script: ' + vulnerability['XSS Script'] + '\n')
            file.write('Input ID: ' + vulnerability['Input ID'] + '\n')
            file.write('Input Name: ' + vulnerability['Input Name'] + '\n')
            file.write('\n')

    # Print the summary
    print(f'Scan finished: {len(vulnerabilities)} vulnerabilities found and saved to {filename}')

# Check if the correct number of arguments is provided
if len(sys.argv) != 3:
    print('Usage: python3 script.py <target_domain> <wordlist_file>')
    sys.exit(1)

# Get the target domain and wordlist file from command-line arguments
target_domain = sys.argv[1]
wordlist_file = sys.argv[2]

# Run the XSS scanning on the target domain with the wordlist
scan_for_xss(target_domain, wordlist_file)
