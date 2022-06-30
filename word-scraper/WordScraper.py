import requests
from bs4 import BeautifulSoup
from collections import Counter
from string import punctuation

get_url = input("[+] Enter the URL to crawl: ")
word_count = input("[+] Enter the number of words to show: ")

# We get the url.
r = requests.get(get_url)
soup = BeautifulSoup(r.content, features="lxml")

# We get the words within paragrphs
text_p = (''.join(s.findAll(text=True))for s in soup.findAll('p'))
c_p = Counter((x.rstrip(punctuation).lower() for y in text_p for x in y.split()))

# We get the words within divs
text_div = (''.join(s.findAll(text=True))for s in soup.findAll('div'))
c_div = Counter((x.rstrip(punctuation).lower() for y in text_div for x in y.split()))

# We sum the two counters and get a list with words count from most to less common.
total = c_div + c_p

list_most_common_words = total.most_common()

# Get X most common words.
common_words = total.most_common(int(word_count))

# Open the txt file.
myfile = open('wordlist.txt', 'w')

# Loop through common words.
for (key, value) in common_words:
    # Add common words to file.
    myfile.write("%s\n" % key)

# Close the file.
myfile.close()
