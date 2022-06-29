import hashlib
import time
import fnmatch
import os

counter = 1
t_time = int(0)

# Get the md5 pass to check against.
md5_pass = input("[+] Enter Your md5 Pass: ")

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
            print("[-] Trying Password %d: %s " % (counter,password.strip()))
            counter += 1
            end = time.time()
            file_time = end - start
            t_time += end - start
            # We found a match.
            if hash_obj == md5_pass:
                print("\n[+] Password Found!!! Password Is: %s " % password)
                print("[-] Total Running Time is:  ", file_time, "seconds")
                break
        # No match found.
        else:
            print("\n[X] Password match not found.")
            print("[-] Closing...")
            print("[-] Total Running Time is:  ",t_time,"seconds")
