# For more details about how this script works, see "Investigative Reversing 2/script.py".

from pwn import unbits

with open("encoded.bmp", "rb") as b:
    b.seek(0x2d3)
    bin_str = ""
    # just like the encoding script, we loop 100 times.
    for j in range(100):
        if ((j & 1) == 0):
            for k in range(8):
                byte = ord(b.read(1))
                bit = byte & 1 # the LSB
                bin_str += str(bit)
        # every other run we skip a byte by just reading and not storing it
        else:
            b.read(1)

char_str = unbits(bin_str, endian='little')
print("Flag: {}".format(char_str.decode("ascii")))