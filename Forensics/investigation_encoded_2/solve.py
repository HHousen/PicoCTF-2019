decoded_dict = {'101011101110111000': 'a', '1010101110111000': 'b', '10111000': 'c', '10101010111000': 'd', '101010101000': 'e', '11101010101000': 'f', '1110111010101000': 'g', '111011101110101000': 'h', '111010101000': 'i', '11101011101000': 'j', '1110101000': 'k', '1010101000': 'l', '101000': 'm', '1011101110111000': 'n', '1010111000': 'o', '101010111000': 'p', '101110111000': 'q', '11101010111000': 'r', '1000': 's', '10111010101000': 't', '1011101110111011101000': 'u', '10111011101011101000': 'v', '1110101110111010111000': 'w', '111010111011101000': 'x', '11101110111010101000': 'y', '1110111010101110111000': 'z', '1110101010111000': '0', '1110101110101110111000': '1', '10111010111010111000': '2', '111010101010111000': '3', '1011101011101000': '4', '101110101011101000': '5', '101011101110101000': '6', '1110101011101000': '7', '1110111011101110111000': '8', '10111011101110111000': '9'}

buffer = ""

# convert the hex to binary and decode it as ascii
# Output of `xxd -c1 output | cut -d" " -f2 | tr -d "\n"`
flag_encoded = bin(0xbaa3aebb8a3aab8eaa3aebb8ea8eaae2eae8eab8eab8eab8eab8eab8eab8eab8eab8eab8eab8eab8eab8bbbb8eeeee2bbb8bbbb8aeee2eae8ebaee00)
# remove the '0b'
flag_encoded = flag_encoded[2:]

flag_decoded = ""

# loop through the bytes in the encoded flag
for idx, bit in enumerate(flag_encoded):
    # add the `bit` to the `buffer`
    buffer += bit
    # if the current buffer decodes to a ascii character...
    if buffer in decoded_dict.keys():
        # ...then add it to the decoded flag...
        flag_decoded += decoded_dict[buffer]
        # ...and clear the buffer, once a character is found
        buffer = ""

print("Flag: {}".format(flag_decoded))