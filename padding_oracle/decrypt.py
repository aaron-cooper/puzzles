from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from os import urandom

key = b'\x0b\x73\xff\x72\x46\xd5\x1c\x22\x3b\x24\xe4\x73\x45\xf5\x56\xde'


with open("cipher.txt", "rb") as infile:
    iv = infile.read(16)
    ciphertext = infile.read()

decryptor = Cipher(algorithms.AES(key), modes.CBC(iv)).decryptor()
plaintext = decryptor.update(ciphertext) + decryptor.finalize()

print(plaintext)