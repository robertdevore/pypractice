import requests

from datetime import date
from datetime import datetime

# datetime object containing current date and time
now = datetime.now()

# Request.
def request(url):
    try:
        return requests.get("https://" + url)
    except requests.exceptions.ConnectionError:
        pass

# Ask the user for the target URL.
targetURL = input("[+] Enter Target URL: ")

# Open the wordlist file.
file = open("common.txt", "r")

# Discovered directories.
df = open("directories-discovered-" + now.strftime("%Y-%m-%d-%H%M%S") + ".txt", "w")

# Start the discovery process.
print("[-] Starting discovery...")

count = 0
lines = 0

try:
    for line in file:
        lines += 1
        print(".")

        line = line.strip("\n")
        fullURL = targetURL + line
        response = request(fullURL)

        ## Directory found.
        if response:
            count += 1
            print('[+] ' + fullURL)
            df.write(str(fullURL))
            df.write('\n')

    df.close()

    print("[+] Searched: " + str(lines))
    print("[+] Discovered: " + str(count))
    print("\n[+] List saved ...")

    print("\n[-] Discovery complete.")

except KeyboardInterrupt:
    print("\n[*] Terminating discovery ... ")

print("[-] Discovery complete")