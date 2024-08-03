# :lock: Content Crypt

Encrypt and decrypt secret messages in the terminal

![python](https://img.shields.io/badge/python-3.x-green.svg) ![license](https://img.shields.io/badge/License-GPLv3-brightgreen.svg)

This project provides a pair of Python scripts for encrypting and decrypting messages using password-based encryption. The scripts utilize the `cryptography` library to ensure secure encryption and decryption processes.

## Requirements

- Python 3.6+
- `cryptography` library

Install the required package using pip:

```
pip install cryptography
```

## :computer: How to use

### Encryption Script (contentEncrypt.py)

This script encrypts a message using a user-provided password.

**Running the script**

```
python contentEncrypt.py
```

**Instructions**

* Enter password: When prompted, enter a password. This password will be used to derive the encryption key.
* Enter message: Provide the message you want to encrypt.
* Save encrypted message: The encrypted message, along with a randomly generated salt, is saved to encrypted.txt.

#### Decryption Script (contentDecrypt.py)

This script decrypts a message encrypted with the corresponding encryption script.

**Command-line Arguments**

*   `filename:`   The path to the file containing the encrypted data (including the salt).
*   `--savefile:` (Optional) The path where the decrypted message will be saved. If not provided, the message will be printed to the console.

**Running the Script**

```
python contentDecrypt.py <filename> [--savefile <output_filename>]
```

**Instructions**

* Enter password: When prompted, enter the password used during encryption.
* Decryption: The script will read the salt and encrypted message from the specified file, derive the key, and decrypt the message.

**Error Handling**

Errors and interruptions are handled gracefully:

* File Not Found: If the specified encrypted file is not found, an error message is displayed.
* Decryption Failure: If the password is incorrect or the file is corrupted, a decryption failure message is shown.
* Script Interruptions: If the script is interrupted, a message is logged, and the process is terminated safely.

### Security Considerations

* Password Strength: Ensure that a strong, unique password is used for encryption to protect the data from brute-force attacks.
* Confidentiality: Do not share the password or the key derived from it. Only those who know the password can decrypt the message.

### License

This project is licensed under the GPLv3 License.