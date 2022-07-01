# :computer: Password cracker

Enter a hashed password and run it against all of your wordlist `.txt` files in the `lists` folder (samples included)

![python](https://img.shields.io/badge/python-3.x-green.svg) ![license](https://img.shields.io/badge/License-GPLv3-brightgreen.svg)

### :computer: How to use

`$ python3 PasswordCracker.py`

### :pray: Thanks

This was forked from [this repo](https://github.com/mayurkadampro/Python-Hash-Cracker). Long live open source :100:

Example lists are from [SecLists](https://github.com/danielmiessler/SecLists).

**TODO:**

*   Create more detailed output along with the total run time, like file names run, total # of hashes checked, etc.
*   Create a way to pass a single file name instead of running all files in the `lists` folder.
*   Create a way to loop through a list of usernames and hashed passwords to check multiple accounts at once (possibly a csv file?)