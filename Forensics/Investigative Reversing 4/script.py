# For more details about how this script works, see "Investigative Reversing 2/script.py".

from pwn import unbits

bin_str = ""
for i in range(5, 0, -1):
    with open("Item0{}_cp.bmp".format(i), "rb") as b:
        b.seek(2019)
        # just like the encoding script, we loop 100 times.
        for j in range(50):
            # read the byte from the flag from 8 bytes of the image using LSB-encoding
            if (j % 5 == 0):
                for k in range(8):
                    byte = ord(b.read(1))
                    bit = byte & 1 # the LSB
                    bin_str += str(bit)
            # after reading the byte of the flag, read 4 bytes of normal image data
            else:
                b.read(1)

char_str = unbits(bin_str, endian='little')
print("Flag: {}".format(char_str.decode("ascii")))