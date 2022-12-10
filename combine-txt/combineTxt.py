import os
import time

# Get the current directory path.
directory = os.path.dirname(os.path.realpath(__file__))

# Define a function that reads a text file and adds each line to a list
def process_file(file_path, lines_list):
    # Open the file in read mode with the latin-1 encoding
    with open(file_path, "r", encoding="latin-1") as f:
        # Read the file lines
        file_lines = f.readlines()

        # Loop through the file lines
        for line in file_lines:
            print(line)
            # Add the line to the list
            lines_list.append(line)

        # Return the updated list
        return lines_list

if __name__ == '__main__':
    # Start the timer
    start = time.perf_counter()
    # Initialize an empty list for the lines
    lines = []

    # Use os.walk() to loop through all the files in the directory
    # and all its subdirectories
    for root, dirs, files in os.walk(directory):
        # Loop through all the files
        for filename in files:
            # Check if the file is a text file
            if filename.endswith(".txt"):
                # Get the full path to the file
                file_path = os.path.join(root, filename)

                # Apply the process_file() function to the file
                lines = process_file(file_path, lines)

    # Use a set() to remove duplicates from the list of lines
    lines = list(set(lines))

    # Save the list of lines to a file
    with open(directory + "/final_list.txt", "w") as f:
        f.writelines(lines)

    # Print a message
    print(f"Finished creating final_list.txt with {len(lines)} unique lines")

    # Stop the timer
    stop = time.perf_counter()

    # Print the time it took to run the script
    print(f"Finished in {stop - start:0.4f} seconds")