import re
import csv
from datetime import datetime

def extract_plugin_info(text):
    plugin_info = {}
    pattern = r'\[PLUGIN\] (.*?) : v(.*?) \('

    for line in text.splitlines():
        if '[PLUGIN]' in line:
            match = re.search(pattern, line)
            if match:
                plugin_name, version_number = match.groups()
                plugin_info[plugin_name] = version_number
    
    return plugin_info

# Prompt the user to enter the file path
file_path = input("Enter the file path: ")

try:
    with open(file_path, 'r') as file:
        input_text = file.read()

        plugin_info = extract_plugin_info(input_text)

        # Save plugin information to a CSV file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file_path = f"plugin_info_{timestamp}.csv"
        with open(output_file_path, 'w', newline='') as output_file:
            writer = csv.writer(output_file)
            writer.writerow(['Plugin', 'Version'])

            for plugin, version in plugin_info.items():
                writer.writerow([plugin, version])

        # Display plugin information in a table in the terminal
        print("\nPlugin Information:")
        print("{:<60} {:<10}".format("Plugin Name", "Version"))
        print("----------------------------------------")
        for plugin, version in plugin_info.items():
            print("{:<60} {:<10}".format(plugin, version))
        print("----------------------------------------")
        print(f"Plugin information saved to {output_file_path}")

except FileNotFoundError:
    print("File not found. Please make sure the file exists and try again.")
