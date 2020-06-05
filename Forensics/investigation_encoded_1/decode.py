import string
# matrix = [
#     0x00000008, 0x00000000, 0x0000000c, 0x00000008, 0x0000000e,
#     0x00000014, 0x0000000a, 0x00000022, 0x00000004, 0x0000002c,
#     0x0000000c, 0x00000030, 0x0000000c, 0x0000003c, 0x0000000a,
#     0x00000048, 0x00000006, 0x00000052, 0x00000010, 0x00000058,
#     0x0000000c, 0x00000068, 0x0000000c, 0x00000074, 0x0000000a,
#     0x00000080, 0x00000008, 0x0000008a, 0x0000000e, 0x00000092,
#     0x0000000e, 0x000000a0, 0x00000010, 0x000000ae, 0x0000000a,
#     0x000000be, 0x00000008, 0x000000c8, 0x00000006, 0x000000d0,
#     0x0000000a, 0x000000d6, 0x0000000c, 0x000000e0, 0x0000000c,
#     0x000000ec, 0x0000000e, 0x000000f8, 0x00000010, 0x00000106,
#     0x0000000e, 0x00000116, 0x00000004, 0x00000124
# ]
matrix = [
    0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0c, 0x00,
    0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x0e, 0x00, 0x00, 0x00,
    0x14, 0x00, 0x00, 0x00, 0x0a, 0x00, 0x00, 0x00, 0x22, 0x00,
    0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x2c, 0x00, 0x00, 0x00,
    0x0c, 0x00, 0x00, 0x00, 0x30, 0x00, 0x00, 0x00, 0x0c, 0x00,
    0x00, 0x00, 0x3c, 0x00, 0x00, 0x00, 0x0a, 0x00, 0x00, 0x00,
    0x48, 0x00, 0x00, 0x00, 0x06, 0x00, 0x00, 0x00, 0x52, 0x00,
    0x00, 0x00, 0x10, 0x00, 0x00, 0x00, 0x58, 0x00, 0x00, 0x00,
    0x0c, 0x00, 0x00, 0x00, 0x68, 0x00, 0x00, 0x00, 0x0c, 0x00,
    0x00, 0x00, 0x74, 0x00, 0x00, 0x00, 0x0a, 0x00, 0x00, 0x00,
    0x80, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x8a, 0x00,
    0x00, 0x00, 0x0e, 0x00, 0x00, 0x00, 0x92, 0x00, 0x00, 0x00,
    0x0e, 0x00, 0x00, 0x00, 0xa0, 0x00, 0x00, 0x00, 0x10, 0x00,
    0x00, 0x00, 0xae, 0x00, 0x00, 0x00, 0x0a, 0x00, 0x00, 0x00,
    0xbe, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0xc8, 0x00,
    0x00, 0x00, 0x06, 0x00, 0x00, 0x00, 0xd0, 0x00, 0x00, 0x00,
    0x0a, 0x00, 0x00, 0x00, 0xd6, 0x00, 0x00, 0x00, 0x0c, 0x00,
    0x00, 0x00, 0xe0, 0x00, 0x00, 0x00, 0x0c, 0x00, 0x00, 0x00,
    0xec, 0x00, 0x00, 0x00, 0x0e, 0x00, 0x00, 0x00, 0xf8, 0x00,
    0x00, 0x00, 0x10, 0x00, 0x00, 0x00, 0x106, 0x00, 0x00, 0x00,
    0x0e, 0x00, 0x00, 0x00, 0x116, 0x00, 0x00, 0x00, 0x04, 0x00,
    0x00, 0x00, 0x124, 0x00, 0x00, 0x00
]
secret = [
    0xb8, 0xea, 0x8e, 0xba, 0x3a, 0x88, 0xae, 0x8e, 0xe8, 0xaa,
    0x28, 0xbb, 0xb8, 0xeb, 0x8b, 0xa8, 0xee, 0x3a, 0x3b, 0xb8,
    0xbb, 0xa3, 0xba, 0xe2, 0xe8, 0xa8, 0xe2, 0xb8, 0xab, 0x8b,
    0xb8, 0xea, 0xe3, 0xae, 0xe3, 0xba, 0x80
]

def getValue(val):
    iVar2 = val
    if (val < 0):
        iVar2 = val + 7

    bVar1 = val >> 0x37
    return secret[iVar2 >> 3] >> (7 - ((val + (bVar1 >> 5) & 7) - (bVar1 >> 5)) & 0x1f) & 1

def encode():
    for character in characters:
        c = ord(character) - 0x61
        decoded_value = ""

        index = matrix[c * 8 + 4]
        end = index + matrix[c*8]

        for i in range(index, end):
            decoded_value += str(getValue(i))

        print(str(character) + ": " + decoded_value)
        decoded_dict[decoded_value] = character


characters = string.ascii_lowercase
decoded_dict = {}
encode()

print("Python dictionary: " + str(decoded_dict))