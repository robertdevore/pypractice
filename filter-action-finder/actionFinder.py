import os
import csv
import re
from datetime import datetime

def find_custom_actions(directory='.'):
    """
    Recursively searches for PHP files in the specified directory and its subdirectories.
    Finds instances of `add_action( 'acme_` and saves action name and file name in a CSV file.
    """
    # List to store action and file information
    results = []

    # Regular expression pattern to find actions
    pattern = re.compile(r"do_action\(\s*'acme_([^']+)'(?:[^,]*)")

    # Iterate through all files and subdirectories
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.php'):
                file_path = os.path.join(root, file)

                with open(file_path, 'r', encoding='utf-8') as php_file:
                    content = php_file.read()
                    matches = pattern.findall(content)
                    for match in matches:
                        results.append({'action_name': 'acme_' + match, 'file_name': file_path})
                        print(f"Instance found in {file_path}: acme_{match}")

    # Create a timestamp for the CSV file name
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    
    # Save results to CSV file with timestamp
    csv_file_path = f'acme_actions_{timestamp}.csv'
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['action_name', 'file_name']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        # Write header
        writer.writeheader()

        # Write data
        writer.writerows(results)

    print(f"Search completed. Results saved to {csv_file_path}")

if __name__ == "__main__":
    # Execute the search
    find_custom_actions()
