import os
import csv
import re
import time

# Get the script start time.
start_time = time.time()

# Get current time.
timestr = time.strftime("%Y%m%d-%H%M%S")

# Set the path to the WordPress root directory.
path = os.path.dirname(__file__)
# Generate the CSV file name.
filename = 'regex-scan-results-' + timestr + '.csv'
# Set the name of the CSV file.
csv_file = os.path.join(path, filename)

# List of regex to use.
regex_list = [
    r"check_ajax_referrer\( '[^']*?', '[^']*?' (?!\s*,\s*'false')\)",
    r"check_ajax_referrer\( '[^']*?', '[^']*?',\s*'false'\)",
    r"check_ajax_referer\([^,]+,[^,]+,\s*false\s*\)",
    r"add_query_arg\(['\"\s]+[^,]+['\"]\s?\)",
    r"^\$[a-zA-Z0-9]*\{([a-zA-Z0-9])\}",
    r"\bphpinfo\(.*\)",
    r"@eval\(\$_POST\['.*'\]\)",
    r"Backdoor",
    r"@include\(\$_GET\['.*'\]\)",
    r"system\(\$_GET\['.*'\]\)",
    r"md5\(\$_GET\['.*'\]\)",
    r"fwrite\(\$fpsetv, getenv\(\"HTTP_COOKIE\"\)\)",
    r"system\"\$cmd 1> /tmp/",
    r"\\145\\166\\141\\154\\050\\142\\141\\163\\145\\066\\064\\137\\144\\145\\143\\157\\144\\145\\050",
    r"\$sh3llColor",
    r"w4ck1ng shell",
    r"private Shell by m4rco",
    r"Shell by Mawar_Hitam",
    r"SHELL_PASSWORD",
    r"ConnectBackShell",
    r"ShellBOT",
    r"== \"bindshell\"",
    r"MagelangCyber",
    r"\/\/rasta\/\/",
    r"Baby_Drakon",
    r"Created By EMMA",
    r"3xp1r3",
    r"NinjaVirus Here",
    r"<dot>IrIsT",
    r"Hacked By EnDLeSs",
    r"Punker2Bot",
    r"Zed0x",
    r"darkminz",
    r"ReaL_PuNiShEr",
    r"OoN_Boy",
    r"Pashkela",
    r"Webcommander at",
    r"YENI3ERI",
    r"d3lete",
    r"Made by Delorean",
    r"Cybester90",
    r"K!LL3r",
    r"MrHazem",
    r"BY MMNBOBZ",
    r"Hackeado",
    r"bgeteam",
    r"VOBRA GANGO",
    r"Asmodeus",
    r"Cautam fisierele de configurare",
    r"BRUTEFORCING",
    r"FaTaLisTiCz_Fx Fx29Sh",
    r"DX_Header_drawn",
    r"Dr\.abolalh",
    r"C0derz\.com",
    r"Mr\.HiTman",
    r"IrSecTeam",
    r"FLoodeR",
    r"eriuqer",
    r"zehirhacker",
    r"freetellafriend\.com",
    r"casus15",
    r"temp_r57_table",
    r"By Psych0",
    r"c99ftpbrutecheck",
    r"d3b~X",
    r"profexor\.hell",
    r"ZOBUGTEL",
    r"The Dark Raver",
    r"<kuku>",
    r"M4ll3r",
    r"itsoknoproblembro",
    r"tmhapbzcerff",
    r"IndoXploit",
    r"FaisaL Ahmed aka rEd X",
    r"eval\/\*[a-z0-9]+\*\/",
    r"eval\([a-z0-9]{4,}\(\$[a-z0-9]{4,}, \$[0-9a-z]{4,}\)\);",
    r"(\(chr\(\d+\^\d+\)\.){4,}",
    r"(\$\_[a-z0-9]{2,}\(\d+\)\.){4,}",
    r"(\$[a-z0-9]{3,}\[\d+\]\.){4,}",
    r"chr\(\d+\)\.""\.""\.""\.""\.""",
    r"(\\[0-9]{3}){6,}",
    r"\$GLOBALS\[\$GLOBALS\['[a-z0-9]{4,}'\]\[\d+\]\.\$GLOBALS\['[a-z-0-9]{4,}'\]\[\d+\]",
    r"\$GLOBALS\['[a-z0-9]{5,}'\] = \$[a-z]+\d+\[\d+\]\.\$[a-z]+\d+\[\d+\]\.\$[a-z]+\d+\[\d+\]\.\$[a-z]+\d+\[\d+\]",
    r"eval\([a-z0-9_]+\(base64_decode\(",
    r"\$[a-z]{3,}=\$[a-z]{3,}\("",\$[a-z]{3,}\);\$[a-z]{3,}\(\);",
    r"Googlebot['\"]{0,1}\s*\)\){echo\s+file_get_contents",
    r"eVaL\(\s*trim\(\s*baSe64_deCoDe\(",
    r"exec\(\"(\\[0-9a-fx]{2,3}){3,}",
    r"if\s*\(\s*mail\s*\(\s*\$mails\[\$i\]\s*,\s*\$tema\s*,\s*base64_encode\s*\(\s*\$text",
    r"fwrite\s*\(\s*\$fh\s*,\s*stripslashes\s*\(\s*@*\$_(GET|POST|SERVER|COOKIE|REQUEST)\[",
    r"echo\s+file_get_contents\s*\(\s*base64_url_decode\s*\(\s*@*\$_(GET|POST|SERVER|COOKIE|REQUEST)",
    r"chr\s*\(\s*101\s*\)\s*\.\s*chr\s*\(\s*118\s*\)\s*\.\s*chr\s*\(\s*97\s*\)\s*\.\s*chr\s*\(\s*108\s*\)",
    r"(\$OOO_O_000_\{\d+\}.){3,}",
    r"chr\s*\(\s*['\"]?\s*((95)|(0[Xx]5[Ff]))\s*['\"]?\s*\)",
    r"['\"][A-Za-z0-9+\/]{260,}={0,3}['\"]",
    r"^.*<\?php.{1100,}\?>.*$",
    r"(\\x[0-9abcdef]{2}[a-z0-9.-\/]{1,4}){4,}",
    r"\/\*[a-z0-9]{5}\*\/",
    r"%\(\d+\-\d+\+\d+\)==\(\-\d+\+\d+\+\d+\)",
    r"\(\$[a-zA-Z0-9]+%\d==\(\d+\-\d+\+\d+\)",
    r"eval\(\$[a-z0-9_]+\(\$_POST",
    r"(\"[a-z0-9]+\"\.chr\(\d+\)\.){3,}",
    r"\$[a-z0-9_]+\(\$[a-z0-9_]+\(",
    r"\$GLOBALS;\$\{\"\\x",
    r"php_uname\([\"'asrvm]+\)",
    r"(\^\s*\$\w+\[\$\w+\s*%\s*strlen\(\$\w+\)\]\s*){2,}",
    r"function\s+_[0-9]{8,}\(",
    r"@include \".*?(\\x[0-9a-f]{2,}.*?){2,}.*?\";",
    r"create_function\s*\(\s*['\"]{2}",
    r"(\$[a-z]{2,}=urldecode\(\$_COOKIE\['[a-z]{2,}'\]\);){3,}",
    r"(\$[A-Z]+\{\d+\}\.){3,}",
    r"\$_REQUEST\s*\/\*[A-Za-z]+\*\/\[",
    r"\(count\(\$p\)==\d+&&in_array\(gettype\(\$p\)\.count\(\$p\),\$p\)\)",
    r"explode\('\|\x01\|\x03\|\x03', gzinflate\(",
    r"@header\(\w{3,5}::\w{1,2}\('_\w{1,3}' \. '\w{1,3}', '_\w{1,3}'\)\);",
    r"@header\(\w{3,5}::\w{1,2}\('_\w{1,3}', '_' \. '\w{1,3}' . '\w{1,3}'\)\);",
    r"@\$[a-z]{1}\[\d+\]\(\$[a-z]{1}\[\d+\]\);",
    r"\$[a-z]11 \^ [a-z]8\(\$[a-z]6, \$[a-z]14, \$[a-z]6\[13\]\(\$[a-z]11\)\)\)\);",
    r"eval\([A-Za-z0-9]{5,}\(\) \. '",
    r"eval\([A-Za-z0-9]{5,}\(\"[A-Z0-9]{16,}",
    r"\$[a-zA-Z0-9]{6,}\('\x78\x9C\xAD\x90\x41\x0E",
    r"return @\$[a-z]{2}\d+\[\d+\]\(\$[a-z]{2}\d+\[\d+\],",
    r"[a-z]{1}\([a-z]{1}\(\$[a-z]{2}\.'\/\.htaccess'\)",
]

## Evil regex.
evil_regex = ["(a+)+", "([a-zA-Z]+)*", "(a|aa)+", "(a|a?)+", r"(.*a){x} for x \> 10"]

# Open the CSV file in write mode.
file = open(csv_file, 'w', newline='')

# Create a CSV writer.
writer = csv.writer(file)

# Add a header row to the CSV file.
writer.writerow(['File', 'Line', 'Code', 'Error'])

# Define the directory to scan
directory = os.path.dirname(os.path.abspath(__file__))

# Counter.
counter = 0

def scan_directory(directory):
    global counter
    # Use os.scandir() to loop through all the files in the directory
    with os.scandir(directory) as entries:
        for entry in entries:
            if entry.is_file() and entry.name.endswith(".php"):
                # Get the full path to the file.
                file_path = entry.path

                # Get the full path to the directory.
                #file_dir = os.path.dirname(file_path)

                # Output line in terminal.
                print(f"Checking: {file_path}")

                # Open the file in read mode
                with open(file_path, "r", encoding='latin-1') as f:

                    # Use the enumerate() function to iterate over the lines in the file
                    for i, line in enumerate(f):

                        # Iterate over the substrings in the list
                        for substring in evil_regex:

                            # Check if the substring is in the line of text
                            if substring in line:

                                # Save the file path, line number, code, and error message to the CSV file.
                                writer.writerow([file_path, i + 1, line.strip()[:100], substring])
                                counter += 1

                        # Iterate over the regex_list items.
                        for regex_item in regex_list:
                            # Search the string for a match to the regular expression
                            match = re.search(regex_item, line)

                            # Did we match?
                            if match:
                                # Save the file path, line number, code, and error message to the CSV file.
                                writer.writerow([file_path, i + 1, line.strip()[:100], match.group(0)])
                                counter += 1
            elif entry.is_dir():
                # Recursively scan the subdirectory
                scan_directory(entry.path)

# Start scanning the directory
scan_directory(directory)

# Close the CSV file.
file.close()

end_time = time.time()

time_elapsed = end_time - start_time

print(f"Scan finished. Found {counter} errors and saved them to the {filename} file.")
print(f"Time elapsed: {time_elapsed:.2f} seconds")
