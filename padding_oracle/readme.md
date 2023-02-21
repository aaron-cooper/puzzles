# Padding Oracle
## Description
### `cipher.txt`
Contains a ciphertext. The ciphertext was encrypted using AES running in CBC mode. The corresponding plaintext will not look random, it'll be obvious when you find it. The plaintext has a sha256 hash of `8d084464e12bb056733cf9d5d5d1cdb96af517e10ab6f3cea0c9d3d0cf208d45`.

### PaddingOracle
Contains two methods:
- an empty constructor
- check(iv, ciphertext) -> bool
    - given a 16 byte IV and a ciphertext whose length is a multiple of 16 bytes, this method
        1. Decrypts ciphertext using AES running in CBC mode.
        2. Returns true of the plaintext has a valid pad as described in sec 6.3 of RFC 5652 or false otherwise.

## Objective
Exploit PaddingOracle to completely recover the plaintext.


## (Suggested) Rules
- Treat the PaddingOracle class as a black box. The source code for padding oracle contains the key used to encrypt the ciphertext, but the challenge is to find the plaintext without knowing the key.
