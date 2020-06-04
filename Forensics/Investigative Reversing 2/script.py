from pwn import unbits

# open the image in "read binary" mode
with open("encoded.bmp", "rb") as data:
    data.seek(2000)
    bin_str = ""
    # loop through the `50 * 8` bytes after 2000.
    # each iteration gives one bit of the flag since one bit of the flag is stored in
    # each byte of the image. so multiply the 50 character flag by 8 bits in a byte to
    # loop through all the bits in the flag.
    for j in range(50 * 8):
        # `data.read(1)` is of type 'bytes' but `data.read(1)[0]` is of type 'int'.
        # file.read() returns a 'bytes' object, which is essentially a list of bytes. ("While bytes
        # literals and representations are based on ASCII text, bytes objects actually behave like
        # immutable sequences of integers." - https://docs.python.org/3/library/stdtypes.html#bytes)
        # since we only read 1 byte at a time, we can safely select the first one in the list.
        # int.from_bytes() can convert a list of bytes to an int and will also work in this case.
        # ord() can also convert a single byte to an int (https://docs.python.org/3/library/functions.html#ord)
        byte = data.read(1)[0]

        # the `&1` selects only the last bit (LSB) in the current byte. it is the bitwise AND operator.
        # see https://en.wikipedia.org/wiki/Bitwise_operation#AND for more information.
        bit = byte & 1
        bin_str += str(bit)

# pwn.unbits docs: https://docs.pwntools.com/en/stable/util/fiddling.html#pwnlib.util.fiddling.unbits
char_str = unbits(bin_str, endian='little')
print("Flag: " + "".join([chr(x + 5) for x in char_str]))