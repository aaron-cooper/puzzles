import argparse
from padding_oracle import *

parser = argparse.ArgumentParser()
parser.add_argument("inputFileName", help="path to file containing ciphertext")
parser.add_argument("outputFileName", help="path for file where plaintext should be stored (contents will be replaced)")
args = parser.parse_args()


BLOCKSIZE = 16

with open(args.inputFileName, "rb") as inputFile:
    iv = inputFile.read(BLOCKSIZE)
    ciphertext = bytearray(inputFile.read())

oracle = PaddingOracle()

remaining = ciphertext[BLOCKSIZE:]
ciphertext = ciphertext[0:BLOCKSIZE]
plaintext = bytearray()

moreCiphertext = True
while moreCiphertext:
    dummyIv = bytearray(b'\x00' * BLOCKSIZE)
    intermediate = bytearray(b'\x00' * BLOCKSIZE)

    # from the end of the block to the beginning
    for i in range(len(dummyIv) - 1, -1, -1):
        # for every possible value j that the ith block can take
        for j in range(256):
            dummyIv[i] = j
            #if we get a valid pad, then the plaintext before it's xor'd with
            #the previous ciphertext (intermediate text) must be padValue xor j
            if oracle.check(dummyIv, ciphertext):
                padValue = BLOCKSIZE - i
                intermediateBit = padValue ^ j
                intermediate[i] = intermediateBit

                #update the already completed elements of dummyIv so that they
                #give an appropriate pad value when xor'd with the intermediate
                #text
                for k in range(i, BLOCKSIZE):
                    dummyIv[k] = intermediate[k] ^ (padValue + 1)
                break

    #now that the intermediate text is known, we can find the real
    #plaintext by xoring each byte of intermediate text with the real
    #iv / previous ciphertext
    for intermediateBit, ivBit in zip(intermediate, iv):
        plaintext.append(intermediateBit ^ ivBit)

    if len(remaining) > 0:
        iv = ciphertext #new iv is previous ciphertext
        ciphertext = remaining[0:BLOCKSIZE]
        remaining = remaining[BLOCKSIZE:]
    else:
        moreCiphertext = False

# plaintext is still padded, so remove the pad
padSize = plaintext[len(plaintext) - 1]
plaintext = plaintext[:-padSize]

with open(args.outputFileName, "wb") as outputFile:
    outputFile.write(plaintext)