import requests
import time
import argparse
from datetime import datetime
from tqdm import tqdm

def check_link(url):
    try:
        response = requests.head(url, allow_redirects=True)
        if response.status_code == 200:
            return True
    except requests.exceptions.RequestException:
        pass
    return False

def create_link_list_file(domain, current_time):
    filename = f"{domain}_link_list_{current_time}.txt"
    with open(filename, "w") as file:
        file.write("Link List:\n")
    return filename

def append_link_to_file(url, domain, current_time):
    filename = f"{domain}_link_list_{current_time}.txt"
    with open(filename, "a") as file:
        file.write(url + "\n")

def process_links(file_path, base_url, passive=False, delay=2):
    with open(file_path, "r") as file:
        lines = file.readlines()

    domain = base_url.split("//")[-1].split("/")[0]
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = create_link_list_file(domain, current_time)

    counter = 0
    pbar = None
    try:
        pbar = tqdm(total=len(lines), desc="Progress")
        for line in lines:
            line = line.strip()
            if line:
                url = base_url.rstrip("/") + "/" + line.lstrip("/")
                if check_link(url):
                    print(f"Valid URL: {url}")
                    append_link_to_file(url, domain, current_time)
                    counter += 1
                if passive:
                    time.sleep(delay)
                pbar.update(1)
    except KeyboardInterrupt:
        print(f"\nUser stopped scan. {counter} results found and saved to {filename}")
    finally:
        if pbar is not None:
            pbar.close()

    print(f"Scan finished. {counter} results found and saved to {filename}")

# Example usage
if __name__ == "__main__":
    print("Starting scanner...")
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", help="Path to the input file")
    parser.add_argument("base_url", help="Base URL to append the lines")
    parser.add_argument("--passive", type=float, help="Enable passive mode with a specified delay in seconds")
    args = parser.parse_args()

    if args.passive:
        process_links(args.file_path, args.base_url, passive=True, delay=args.passive)
    else:
        process_links(args.file_path, args.base_url)
