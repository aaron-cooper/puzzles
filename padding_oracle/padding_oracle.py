from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

class PaddingOracle:
    def __init__(self):
        self.key = b'\x0b\x73\xff\x72\x46\xd5\x1c\x22\x3b\x24\xe4\x73\x45\xf5\x56\xde'

    # given an IV and a ciphertext, returns true if the corresponding plain
    # text has valid padding as defined in section 6.3 of RFC 5652
    def check(self, iv: bytes, ciphertext: bytes):
        decryptor = Cipher(algorithms.AES(self.key), modes.CBC(iv)).decryptor()
        padded = decryptor.update(ciphertext) + decryptor.finalize()
        padSize = padded[len(padded) - 1]
        # padSize is in 1..16 and the last padSize bytes in the plaintext
        # == padSize
        return (1 <= padSize and padSize <= 16
            and all(map(lambda b: b == padSize, padded[-padSize:])))