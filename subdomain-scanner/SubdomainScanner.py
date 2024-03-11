import requests
import time
import urllib3
import sys
import argparse
import csv
from datetime import datetime
import os

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--domain", type=str, required=True, help="Target Domain.")
    parser.add_argument("-o", "--output", type=str, required=False, help="Output to file.")
    return parser.parse_args()

def banner():
    print("Name: Subdomain Scanner")
    print("Version: 0.0.1")
    print("Copyright: Robert DeVore")
    time.sleep(1)

def parse_url(url):
    try:
        host = urllib3.util.url.parse_url(url).host
    except Exception as e:
        print("[*] Invalid domain, try again..")
        print(f"[*] ERROR: {e}")
        sys.exit(1)
    return host

def write_subs_to_file(subdomains, output_file):
    with open(output_file, "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        for subdomain in subdomains:
            csvwriter.writerow([subdomain])

def main():
    banner()
    subdomains = []

    args = parse_args()
    target = parse_url(args.domain)
    output = args.output

    req = requests.get(f"https://crt.sh/?q=%.{target}&output=json")

    if req.status_code != 200:
        print("[X] Information not available!")
        sys.exit(1)

    for (key, value) in enumerate(req.json()):
        subdomain = value["name_value"].strip()
        if not (subdomain.startswith('"') and subdomain.endswith('"')):
            subdomains.append(subdomain)

    print(f"\n[!] Target: {target}\n")

    subs = sorted(set(subdomains))

    if output is None:
        for s in subs:
            print(f"{s}\n")

    if output is not None:
        now = datetime.now()
        date_time = now.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"subdomain-scanner-{target}-{date_time}.csv"
        current_directory = os.getcwd()
        output_file_path = os.path.join(current_directory, filename)
        write_subs_to_file(subs, output_file_path)
        print(f"\n[+] Subdomains saved to: {output_file_path}")

    print("\n\n[+] Subdomain Scanner is complete. All subdomains have been found.")

if __name__ == "__main__":
    main()
