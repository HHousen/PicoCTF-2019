decoded_dict = {'10111000': 'a', '111010101000': 'b', '11101011101000': 'c', '1110101000': 'd', '1000': 'e', '101011101000': 'f', '111011101000': 'g', '1010101000': 'h', '101000': 'i', '1011101110111000': 'j', '111010111000': 'k', '101110101000': 'l', '1110111000': 'm', '11101000': 'n', '11101110111000': 'o', '10111011101000': 'p', '1110111010111000': 'q', '1011101000': 'r', '10101000': 's', '111000': 't', '1010111000': 'u', '101010111000': 'v', '101110111000': 'w', '11101010111000': 'x', '1110101110111000': 'y', '11101110101000': 'z'}

buffer = ""

# convert the hex to binary and decode it as ascii
# Output of `xxd -c1 output | cut -d" " -f2 | tr -d "\n"`
flag_encoded = bin(0x8e8eba3bb8ea23a8a8ba3a8eee38eea3a8eb8aa3ab80)
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