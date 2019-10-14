# AES-ABC

## Problem

> AES-ECB is bad, so I rolled my own cipher block chaining mechanism - Addition Block Chaining! You can find the source here: aes-abc.py. The AES-ABC flag is body.enc.ppm

* [Source](./aes-abc.py)
* [Source](./body.enc.ppm)

## Solution

1. Header is the first three lines of `body.enc.ppm` so save those.
2. For the actual picture info extract from bytes to ints in blocks of 16 since that is what the [encryption script](./aes-abc.py) does.
3. The [encryption script](./aes-abc.py) encodes blocks by doing `(previous block + current block) % UMAX` so the [decryption script](./script.py) does the opposite: `(current - previous) % UMAX`.
4. Run that for each block and convert back to bytes.
5. Copy the file header to a new image and append each block to that image.
6. See [ebc.png](./ebc.png) for example on why we don't bother decrypting ebc. More info at [Wikipedia](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation)

### Flag

`picoCTF{d0Nt_r0ll_yoUr_0wN_aES}`