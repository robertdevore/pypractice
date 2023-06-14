import os
from datetime import datetime

from bs4 import BeautifulSoup
import requests
import requests.exceptions
import urllib.parse
from collections import deque
import re

use_url = str(input('[+] Enter Target URL to Scan: '))
urls = deque([use_url])

scraped_urls = set()
emails = set()
telephone_numbers = set()

count = 0
try:
    while len(urls):
        count += 1
        if count == 100:
            break
        url = urls.popleft()
        scraped_urls.add(url)

        parts = urllib.parse.urlsplit(url)
        base_url = '{0.scheme}://{0.netloc}'.format(parts)

        path = url[:url.rfind('/') + 1] if '/' in parts.path else url

        print("[{0}] Processing '{1}'".format(count, url))

        try:
            response = requests.get(url)
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            continue

        new_email = set(re.findall(r'[a-z0-9.\-+_]+@[a-z0-9.\-+_]+\.[a-z]+', response.text, re.I))
        filtered_email = [email for email in new_email if not re.search(r'\.(jpeg|jpg|png|gif|tiff|webp|mov|webm)$', email)]
        emails.update([(url, email) for email in filtered_email])

        new_telephone = set(re.findall(r'tel:(\+?[0-9\-]+)', response.text))
        telephone_numbers.update(new_telephone)

        soup = BeautifulSoup(response.text, features="lxml")

        for anchor in soup.find_all("a"):
            link = anchor.attrs['href'] if 'href' in anchor.attrs else ''
            if link.startswith('/'):
                link = base_url + link
            elif not link.startswith('http'):
                link = urllib.parse.urljoin(path, link)

            # Check if the link is a telephone number link
            if link.startswith('tel:'):
                telephone_numbers.add(link)
                print("Skipping telephone number link: {}".format(link))
                continue

            if not link in urls and not link in scraped_urls:
                urls.append(link)
except KeyboardInterrupt:
    print('[-] Closing ... ')

# Get domain name from the URL
domain_name = urllib.parse.urlparse(use_url).netloc

# Get the current time
current_time = datetime.now().strftime("%Y%m%d%H%M%S")

# Create the file names with domain and time
emails_file = "emails-{}-{}.txt".format(domain_name, current_time)
telephone_file = "telephone-{}-{}.txt".format(domain_name, current_time)

# Save email addresses to the emails file
with open(emails_file, "w") as f:
    # Write header line
    f.write("URL, Email\n")
    
    for url, email in emails:
        f.write("{}, {}\n".format(url, email))

# Save telephone numbers to the telephone numbers file
with open(telephone_file, "w") as f:
    for number in telephone_numbers:
        f.write(number + "\n")

print("Process complete. Email addresses saved to '{}' file. Telephone numbers saved to '{}' file. Goodbye.".format(emails_file, telephone_file))
