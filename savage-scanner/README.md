# :mag_right: Savage Scanner

Provide a wordlist to perform bruteforce recon on a domain in order to find vulnerable URL's

![python](https://img.shields.io/badge/python-3.x-green.svg) ![license](https://img.shields.io/badge/License-GPLv3-brightgreen.svg)

### :computer: How to use

`$ python3 savageScanner.py wordlist.txt domain.com`

You can also apply a passive flag in order to set how many seconds between URL checks in order to avoid being rate limited.

`$ python3 savageScanner.py wordlist.txt domain.com --passive 2`
