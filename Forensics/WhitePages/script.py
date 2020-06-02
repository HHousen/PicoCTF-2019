from pwn import *

with open('whitepages.txt', 'rb') as f:
    data = f.read()  # data is a bytearray

# Replace the unicode EM SPACE (0xE2 0x80 0x83) with the byte for "0"
# Replace the standard space (0x20) with the byte for "1"
data = data.replace(b'\xe2\x80\x83', b'0').replace(b' ', b'1')

# Convert from bytes to ascii since that is the format the `unbits()` function accepts
data = data.decode("ascii")

# `unbits()` takes a list of bits (or something that can be decoded to a bit) and converts
# them into a string of bytes. We decode this string of bytes to ascii so it can be nicely printed.
print(unbits(data).decode("ascii"))