from cryptography.fernet import Fernet

keyFile = 'symKey.key'
key = Fernet.generate_key()
with open(keyFile, 'wb') as f:
    f.write(key)

