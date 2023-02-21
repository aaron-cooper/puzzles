from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from os import urandom

key = b'\x0b\x73\xff\x72\x46\xd5\x1c\x22\x3b\x24\xe4\x73\x45\xf5\x56\xde'
iv = b'\x8c\xc5\x14\x9a\xe0\x99\xf0\x93\xe3\xe2\xe3\x40\x68\x26\x40\x93'

encryptor = Cipher(algorithms.AES(key), modes.CBC(iv)).encryptor()

with open("plaintext.txt", "rb") as infile:
    data = infile.read()

pad_req = 16 - len(data) % 16
pad = pad_req.to_bytes(1, 'little') * pad_req

data += pad

ct = encryptor.update(data) + encryptor.finalize()

with open("cipher.txt", 'wb') as outfile:
    outfile.write(iv)
    outfile.write(ct)