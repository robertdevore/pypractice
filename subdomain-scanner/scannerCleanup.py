import csv
import os
from datetime import datetime
import argparse

def clean_data(input_file, output_file):
    # Function to clean the data from input_file and save to output_file
    
    # Initialize a set to store cleaned data (to automatically remove duplicates)
    cleaned_data = set()
    
    # Read the CSV file
    with open(input_file, 'r', newline='') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            # Split the line by whitespace to handle multiple subdomains
            subdomains = row[0].split()
            
            # Loop through each subdomain
            for subdomain in subdomains:
                # Remove double quotes at the beginning and end of each subdomain
                cleaned_subdomain = subdomain.strip('"\n ')
                
                # Check if the cleaned_subdomain is not empty after stripping
                if cleaned_subdomain:
                    cleaned_data.add(cleaned_subdomain)
    
    # Convert the set to a sorted list
    cleaned_data = sorted(cleaned_data)
    
    # Write the cleaned data to a new CSV file
    with open(output_file, 'w', newline='') as csv_output:
        writer = csv.writer(csv_output)
        for domain in cleaned_data:
            writer.writerow([domain])
    
    print(f"Cleaned data saved to {output_file}")

def main():
    # Main function to run the script
    
    # Setup argument parser
    parser = argparse.ArgumentParser(description="Clean data in CSV file")
    parser.add_argument("-f", "--file", help="Input CSV file name", required=True)
    args = parser.parse_args()
    
    # Input and output file paths
    input_file = args.file
    
    # Generate the output file name with domain and timestamp
    domain = os.path.splitext(os.path.basename(input_file))[0]
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_file = f"{domain}-{timestamp}.csv"
    
    # Call the clean_data function
    clean_data(input_file, output_file)

if __name__ == "__main__":
    main()
