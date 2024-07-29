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
    parser.add_argument("-o", "--output", type=str, choices=["print", "file"], default="print", help="Output method: 'print' or 'file'. Default is 'print'.")
    return parser.parse_args()

def banner():
    print("Name: Subdomain Scanner")
    print("Version: 0.0.2")
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
    cleaned_data = set()

    for subdomain in subdomains:
        cleaned_subdomain = subdomain.strip('"\n ')
        
        if cleaned_subdomain:
            cleaned_data.add(cleaned_subdomain)

    cleaned_data = sorted(cleaned_data)

    print(f"[+] Writing to file: {output_file}")
    with open(output_file, "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        for subdomain in cleaned_data:
            csvwriter.writerow([subdomain])
    print(f"[+] File written successfully: {output_file}")

def main():
    banner()
    subdomains = []

    args = parse_args()
    target = parse_url(args.domain)
    output_method = args.output

    print(f"\n[!] Target: {target}\n")

    print("[+] Starting scan...\n")

    try:
        req = requests.get(f"https://crt.sh/?q=%.{target}&output=json")
        req.raise_for_status()
    except requests.RequestException as e:
        print(f"[X] Request failed: {e}")
        sys.exit(1)

    if req.status_code != 200:
        print(f"[X] Unexpected status code: {req.status_code}")
        sys.exit(1)

    try:
        response_json = req.json()
    except ValueError as e:
        print(f"[X] Failed to parse JSON response: {e}")
        print(f"[X] Response content: {req.text}")
        sys.exit(1)

    for value in response_json:
        subdomain = value["common_name"].strip()
        if not (subdomain.startswith('"') and subdomain.endswith('"')):
            subdomains.append(subdomain)

    subs = sorted(set(subdomains))

    if output_method == "print":
        for s in subs:
            print(f"[*] {s}")
    elif output_method == "file":
        now = datetime.now()
        date_time = now.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"subdomain-scanner-{target}-{date_time}.csv"
        current_directory = os.getcwd()
        scans_directory = os.path.join(current_directory, "scans")
        
        if not os.path.exists(scans_directory):
            print(f"[+] Creating scans directory: {scans_directory}")
            os.makedirs(scans_directory)
        
        output_file_path = os.path.join(scans_directory, filename)
        print(f"[+] Output file path: {output_file_path}")
        write_subs_to_file(subs, output_file_path)
        print(f"[+] Results saved to: {output_file_path}")

    print("\n[+] Subdomain Scanner is complete. All subdomains have been found.")

if __name__ == "__main__":
    main()
