# Import scapy
import scapy.all as scapy
# We need to create regular expressions to ensure that the input is correctly formatted.
import re

# Basic user interface header.
print(r"""
     __     _                      _      __                                 
  /\ \ \___| |___      _____  _ __| | __ / _\ ___ __ _ _ __  _ __   ___ _ __ 
 /  \/ / _ \ __\ \ /\ / / _ \| '__| |/ / \ \ / __/ _` | '_ \| '_ \ / _ \ '__|
/ /\  /  __/ |_ \ V  V / (_) | |  |   <  _\ \ (_| (_| | | | | | | |  __/ |   
\_\ \/ \___|\__| \_/\_/ \___/|_|  |_|\_\ \__/\___\__,_|_| |_|_| |_|\___|_| v0.0.1
 """)
print("\n****************************************************************")
print("* Robert DeVore                                                *")
print("* https://www.robertdevore.com                                 *")
print("* https://www.github.com/robertdevore                          *")
print("****************************************************************")

# Regular Expression Pattern to recognise IPv4 addresses.
ip_add_range_pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}/[0-9]*$")

# Get the address range to ARP.
while True:
    ip_add_range_entered = input("\n[+] Enter IP address and range (ex 192.168.1.0/24): ")
    print(" ")
    if ip_add_range_pattern.search(ip_add_range_entered):
        print(f"{ip_add_range_entered} is a valid ip address range")
        break

# Try ARPing the ip address range supplied by the user. 
# The arping() method in scapy creates a pakcet with an ARP message 
# and sends it to the broadcast mac address ff:ff:ff:ff:ff:ff.
# If a valid ip address range was supplied the program will return 
# the list of all results.
arp_result = scapy.arping(ip_add_range_entered)

print("Network Scanner process complete. Goodbye.")