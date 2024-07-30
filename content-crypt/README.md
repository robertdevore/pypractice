# :lock: Content Crypt

Encrypt and decrypt secret messages

![python](https://img.shields.io/badge/python-3.x-green.svg) ![license](https://img.shields.io/badge/License-GPLv3-brightgreen.svg)

### :computer: How to use

**Encrypt Message**

`$ python3 contentCrypt.py`

You'll be prompted to enter a password which is used to create the key used for the encryption

Then you'll be prompted to enter the message you'd like to encrypt.

The secret message will be saved to a file named `encrypted.txt`

**Deccrypt Message**

`$ python3 contentDecrypt.py encrypted.txt`

You'll be prompted to enter the password to decrypt the message which will output to the terminal.

Alternately, you can pass a `--savefile` flag with a name of the file you'd like the decrypted message to save to.

`$ python3 contentDecrypt.py encrypted.txt --savefile decrypted.txt`