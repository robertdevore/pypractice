from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode
import os
import getpass
import sys

def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return urlsafe_b64encode(kdf.derive(password.encode()))

def main():
    try:
        # Get password from user
        password = getpass.getpass(prompt="Enter password: ")

        # Generate a random salt
        salt = os.urandom(16)
        key = derive_key(password, salt)

        # Encrypt the message
        data = getpass.getpass(prompt="[-] Write the message you would like to encrypt: ")
        data = bytes(data, 'utf-8')
        f = Fernet(key)
        encrypted = f.encrypt(data)

        # Save the salt and encrypted message
        with open("encrypted.txt", "wb") as file:
            file.write(salt + encrypted)
        print("Encrypted message has been saved to 'encrypted.txt'.")

    except KeyboardInterrupt:
        print("\nScript interrupted by user.")
        with open("error_log.txt", "w") as error_file:
            error_file.write("Script interrupted by user.\n")
        sys.exit(1)
    except Exception as e:
        print("An error occurred:", e)
        with open("error_log.txt", "w") as error_file:
            error_file.write(f"Error: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
