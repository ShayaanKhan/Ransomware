import os
from pathlib import Path
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Private key in PEM format
# privKey = '''MIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDgCpIWc+OJny2Tf/sBzCzydlbtGtjLnChVbvSXD00lbL5VjcF0y6QfjhEx9JqKA3msnYE3xSSyi5z5lYK0fYgaboSG0Gfose/zMAqk8LAaQQKrYqdGFapmSC80zWJkB/acHg0u2R61t5ExZdcehPwEWFlJ26pUiqnDSkz1/g2zUaCX6Bw3Pot+Avmcl0zaic9dWYEHBoeFDHa+Z+/Jo3RoHNbWzMtERXh3LAX2Ls3xuNUIKisoGGFvJoWcsp9pTQXQotDdtFtV6piaBv8NfIdo7my+Mu53BpO7G4aseVQmw3J98pZWiK1sG75K3y3K1aQquZMk4h8BvtGjS8r60eBrAgMBAAECggEABP4zwprIk0ZDqTSlvRagyyRNk2oQ+iYC4zcztOxbJzrr9hol4MyV7B6NanCYUYpsSW5sSng6LiR5R+RyjdGkJ2xsqwMnHa2zSLq6lY453LaXTTHV/EnBw94BhYq7IA/N0Ng2m6qQLaU84a+5rQmrO7fHcvi182gpfCm0E9NhvFa755236gsEaYNXZoAncqX8ZZlR6KR8l8VyUC0YLto+jBHg7sqRE2XnWLSDummX+2+9W8bMKwti+013bODU0PvO4KP6FEltjtut5uTwgTCVVjGiTniaOdh0WH8q5FmnQb/YHnG7ei4VuPXmSjpFSxk+W0wwT9HcW8YUW1cQURcDCQKBgQD7HPUlHoH0EUy+BXkIPFtatd6HlN/AzDI2q9hHBpUHjLJDCvrJj9cUoIw0m0AT7gSIHobAHinnaiCR7nFItmBkjxnFLZ5/aln4vM4RjdEWZjrskgiENUBtXkizBrDg84+7xMJCWAYNh3ov+/FIB9t3l3dW9AxAuvEaG9lusDfaTQKBgQDkZr3Xc9VrnDJD6hUQu2Bhwh0N8LWLuczHN8PZEccTjDbj1pSWCII9rWaBK2pTAWWFTMc0G5h4Vz8Uv1QvhyvU2EJSgu5fDeCcm9BawDHYF59fg4v/2C19drad+xrq/6I9DQkeePfrrqJtZIG9K1P4yyJxPUnolaPNmUVHBGURlwKBgQC83VO3nlFpSxWoGZ+lRRgEiqMa4CrF7A6cNfVNvjKaYgS1De3/aVL/7Zxl+JpiIvN/mU4J8uXbamOivm6vnJO1LjfYqG38MPYIcaCfbUVkDnGk+lSzcwXI/E+7bn3cQvPI6rycf23WAR4yNtCLN3WmZeJZIOaSTMgHtgh8CseHRQKBgQDPNWaFUFEOj2YKtxLlWxjVl4VEYFxTpvxgv/att7MjyNEDYmjqtE10JxwXk4uiQmIXzM/sNhzdEEnqSKnXdIoPTyLcOGyJT822RqV/r12I7eVoga9BLJ4YdNq3+FczWzeUq37aZmSFLKmvFL+fHu/Phnp4wWGL4DX7EFIJW7NVgQKBgQDggtij5NNKBsuAgyc6l5PNs0MMXusnprLiHLpqtXOASco8cw45Uz98iMG609S87nbsgFf9CTcRZg7AqPdrjlwMICqMghf5iCLAI0ebHfSUrms0XeufECnGO7aG+vjePTWzdGUS+iXk+uZEeg3kA6Lj7FTuITgvxM1BMFvpBVWYLQ=='''
def decrypt(dataFile, privateKeyFile):
    # Read data from file
    with open(dataFile, 'rb') as f:
        data = f.read()

    # Load RSA private key
    with open(privateKeyFile, 'rb') as key_file:
        private_key = serialization.load_pem_private_key(key_file.read(), password=None, backend=default_backend())

    # Split the encrypted file into components
    encryptedSessionKey = data[:private_key.key_size // 8]
    ciphertext = data[private_key.key_size // 8:]

    # Decrypt the session key with the private key
    sessionKey = private_key.decrypt(
        encryptedSessionKey,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Decrypt data with session key
    cipher = Cipher(algorithms.AES(sessionKey), modes.CFB(sessionKey))
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    # Save the decrypted data to file
    decryptedFile = dataFile.replace('.skillissue', '')
    with open(decryptedFile, 'wb') as f:
        f.write(plaintext)

def scanRecurse(baseDir):
    for entry in os.scandir(baseDir):
        if entry.is_file() and entry.name.endswith('.skillissue'):
            yield entry
        elif entry.is_dir():
            yield from scanRecurse(entry.path)

privateKeyFile = 'private_key.pem'
# Decrypt all skillissue files in the current directory and its subdirectories
directory = './'  # Change this to the directory containing the skillissue files
for item in scanRecurse(directory):
    decrypt(item, privateKeyFile)

print("Decryption completed successfully.")
