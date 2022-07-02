import hashlib
import time
import fnmatch
import os

counter = 1
t_time = int(0)

# Basic user interface header.
print(r"""
   ___                                    _     ___               _             
  / _ \__ _ ___ _____      _____  _ __ __| |   / __\ __ __ _  ___| | _____ _ __ 
 / /_)/ _` / __/ __\ \ /\ / / _ \| '__/ _` |  / / | '__/ _` |/ __| |/ / _ \ '__|
/ ___/ (_| \__ \__ \\ V  V / (_) | | | (_| | / /__| | | (_| | (__|   <  __/ |   
\/    \__,_|___/___/ \_/\_/ \___/|_|  \__,_| \____/_|  \__,_|\___|_|\_\___|_| v0.0.1
 """)
print("\n****************************************************************")
print("* Robert DeVore                                                *")
print("* https://www.robertdevore.com                                 *")
print("* https://www.github.com/robertdevore                          *")
print("****************************************************************")

# Get the md5 hash to check against.
md5_pass = input("[+] Enter the md5 hash: ")

# Lets begin.
try:
    # Loop through files in 'lists' directory.
    for file in os.listdir('./lists'):
        # Make sure we are only running on txt files.
        if fnmatch.fnmatch(file, '*.txt'):
            # Get the current file in the loop.
            md5_file = open('./lists/' + file,"r")
            # loop through eack line in txt file.
            for password in md5_file:
                hash_obj = hashlib.md5(password.strip().encode('utf-8')).hexdigest()
                start = time.time()
                print("[-] %d: %s " % (counter,password.strip()))
                counter += 1
                end = time.time()
                file_time = end - start
                t_time += end - start
                # We found a match.
                if hash_obj == md5_pass:
                    print("\n[+] Password Found!!! Password Is: %s " % password)
                    print("\n[-] Tried: ",counter)
                    print("[-] Runtime: ", file_time, "seconds")
                    break
            # No match found.
            else:
                print("\n[X] Password match not found.")
                print("[-] Closing...")
                print("[-] Total Running Time is:  ",t_time,"seconds")
# Display data if user closes out task early (CTRL+C, for example).
except KeyboardInterrupt:
    print("\n[*] Terminating password craker ... ")
    print("\n[-] Tried: ",counter)
    print("[-] Runtime:  ",t_time,"seconds")

print("\nProcess complete. Goodbye.")