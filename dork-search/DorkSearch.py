import sys
import time
from googlesearch import search

# The domain name to append to the google dork searches.
domain = input("[+] Enter the domain name to target: ")
if not domain:
    domain = ""
else:
    domain = "site:" + domain + " "

# The amount of results to return.
amount_input = input("[+] Enter the amount of results to return: ")
if not amount_input:
    amount = 10
else:
    amount = amount_input

# The dork file name to use in the searches.
dork_file = input("[+] Enter the dork filename to use: ")
if not dork_file:
    dork_file = ""
else:
    dork_file = dork_file

# Let's get started.
print("\n[-] Starting dork search.")

time.sleep(1)

try:
    # Let's build a dorks array.
    dorks = []
    dork_count = 0
    d = open(dork_file)

    print("[-] Building the dorks list.")

    time.sleep(1)

    # Loop through dorks file.
    for ddork in d:
        dork_count += 1
        dorks.append(ddork)
        if dork_count >= int(amount):
            break
    d.close()

    time.sleep(1)

    print("[-] Dorks list has been created.")

    time.sleep(1)

    print("[-] Looping through available dorks.")

    # Loop through dorks.
    for dork in dorks:
        # Data array.
        data = []
        print("\n[-] Searching for: " + dork.strip())
        # Create variables.
        counter = 0
        requ = 0
        time.sleep(1)
        # Loop through results.
        for results in search(domain + dork.strip(), tld="com", lang="en", num=int(amount), start=0, stop=int(amount), pause=6):
            # Update counters.
            counter = counter + 1
            requ += 1
            # Add data to array.
            new = (results)
            data.append(new)
            # Stop at the amount requested.
            if requ >= int(amount):
                break
        # Check for results.
        if not data:
            print("[x] No results found.")
        else:
            # Open the txt file.
            myfile = open('results.txt', 'a+')
            time.sleep(1)
            print("[-] Saving results to file (this could take a while)...\n")
            # Print dork to file.
            myfile.write("# DORK: %s\n" % dork)
            # Loop through results.
            for link in data:
                # Add links to file.
                myfile.write("%s\n" % link)
                print(link)
            #Add line break after links
            myfile.write("\n")
            # Close the file.
            myfile.close()
            print("\n")
except KeyboardInterrupt:
    print("\n[*] Terminating process.")

print("\nResults complete. Goodbye.")
