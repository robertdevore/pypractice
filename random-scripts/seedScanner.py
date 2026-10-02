import argparse
import csv
import os
import re


def count_words(text):
    # Using regex to count words, considering words as continuous sequences of non-whitespace characters
    words = re.findall(r'\S+', text)
    return len(words)

def find_files_with_12_words(directory):
    txt_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    word_count = count_words(content)
                    if word_count == 12:
                        txt_files.append(file_path)
    return txt_files


def save_to_csv(file_list, output_file):
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["File Paths"])
        for path in file_list:
            writer.writerow([path])


def parse_args():
    parser = argparse.ArgumentParser(
        description="Find text files containing exactly 12 words."
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=os.path.dirname(os.path.abspath(__file__)),
        help="folder to scan recursively (defaults to the script's folder)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    search_directory = os.path.abspath(os.path.expanduser(args.directory))

    if not os.path.isdir(search_directory):
        raise SystemExit(f"Directory not found: {search_directory}")

    # Call function to find files with exactly 12 words
    twelve_word_files = find_files_with_12_words(search_directory)

    # Print the list of files
    if twelve_word_files:
        print("Files with exactly 12 words:")
        for file in twelve_word_files:
            print(file)
    else:
        print("No files with exactly 12 words found.")

    # Save the list to a CSV file
    if twelve_word_files:
        output_file = "twelve_word_files.csv"
        save_to_csv(twelve_word_files, output_file)
        print(f"List of files saved to {output_file}")


if __name__ == "__main__":
    main()
