from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode
import getpass
import os
import sys
import argparse

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
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Decrypt an encrypted file.")
    parser.add_argument("filename", help="The file containing the encrypted data")
    parser.add_argument("--savefile", help="Save the decrypted message to a specified file", type=str)
    args = parser.parse_args()

    filename = args.filename
    savefile = args.savefile

    try:
        # Get password from user
        password = getpass.getpass(prompt="Enter password: ")

        # Read the salt and encrypted message from the file
        if not os.path.isfile(filename):
            raise FileNotFoundError(f"The file '{filename}' does not exist.")

        with open(filename, "rb") as file:
            salt = file.read(16)  # First 16 bytes are the salt
            encrypted_data = file.read()

        # Derive the key from the password and salt
        key = derive_key(password, salt)
        f = Fernet(key)

        # Decrypt the message
        try:
            decrypted_data = f.decrypt(encrypted_data).decode('utf-8')
            
            if savefile:
                # Save the decrypted message to a specified file
                with open(savefile, "w") as file:
                    file.write(decrypted_data)
                print(f"Decrypted message has been saved to '{savefile}'.")
            else:
                # Print the decrypted message to the terminal
                print(decrypted_data)
                
        except Exception as decryption_error:
            print("Failed to decrypt message:", decryption_error)
            with open("error_log.txt", "w") as error_file:
                error_file.write(f"Decryption failed: {decryption_error}\n")
                
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
