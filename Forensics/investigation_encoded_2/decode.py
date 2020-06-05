import string

indexTable = [
    0x00000000, 0x00000004, 0x00000012, 0x00000028, 0x0000003c,
    0x00000052, 0x00000064, 0x00000078, 0x0000008e, 0x0000009e,
    0x000000b4, 0x000000c8, 0x000000da, 0x000000ea, 0x000000fc,
    0x0000010e, 0x0000011e, 0x00000134, 0x00000148, 0x0000015a,
    0x0000016a, 0x00000172, 0x00000180, 0x0000018c, 0x0000019a,
    0x000001aa, 0x000001bc, 0x000001c8, 0x000001d6, 0x000001e0,
    0x000001ea, 0x000001f0, 0x00000200, 0x0000020a, 0x00000216,
    0x00000222, 0x00000230, 0x00000234
]

# indexTable = [
#     0x00, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x12, 0x00,
#     0x00, 0x00, 0x28, 0x00, 0x00, 0x00, 0x3c, 0x00, 0x00, 0x00,
#     0x52, 0x00, 0x00, 0x00, 0x64, 0x00, 0x00, 0x00, 0x78, 0x00,
#     0x00, 0x00, 0x8e, 0x00, 0x00, 0x00, 0x9e, 0x00, 0x00, 0x00,
#     0xb4, 0x00, 0x00, 0x00, 0xc8, 0x00, 0x00, 0x00, 0xda, 0x00,
#     0x00, 0x00, 0xea, 0x00, 0x00, 0x00, 0xfc, 0x00, 0x00, 0x00,
#     0x10e, 0x00, 0x00, 0x00, 0x11e, 0x00, 0x00, 0x00, 0x134, 0x00,
#     0x00, 0x00, 0x148, 0x00, 0x00, 0x00, 0x15a, 0x00, 0x00, 0x00,
#     0x16a, 0x00, 0x00, 0x00, 0x172, 0x00, 0x00, 0x00, 0x180, 0x00,
#     0x00, 0x00, 0x18c, 0x00, 0x00, 0x00, 0x19a, 0x00, 0x00, 0x00,
#     0x1aa, 0x00, 0x00, 0x00, 0x1bc, 0x00, 0x00, 0x00, 0x1c8, 0x00,
#     0x00, 0x00, 0x1d6, 0x00, 0x00, 0x00, 0x1e0, 0x00, 0x00, 0x00,
#     0x1ea, 0x00, 0x00, 0x00, 0x1f0, 0x00, 0x00, 0x00, 0x200, 0x00,
#     0x00, 0x00, 0x20a, 0x00, 0x00, 0x00, 0x216, 0x00, 0x00, 0x00,
#     0x222, 0x00, 0x00, 0x00, 0x230, 0x00, 0x00, 0x00, 0x234, 0x00,
#     0x00, 0x00
# ]
secret = [
    0x8b, 0xaa, 0x2e, 0xee, 0xe8, 0xbb, 0xae, 0x8e, 0xbb, 0xae,
    0x3a, 0xee, 0x8e, 0xee, 0xa8, 0xee, 0xae, 0xe3, 0xaa, 0xe3,
    0xae, 0xbb, 0x8b, 0xae, 0xb8, 0xea, 0xae, 0x2e, 0xba, 0x2e,
    0xae, 0x8a, 0xee, 0xa3, 0xab, 0xa3, 0xbb, 0xbb, 0x8b, 0xbb,
    0xb8, 0xae, 0xee, 0x2a, 0xee, 0x2e, 0x2a, 0xb8, 0xaa, 0x8e,
    0xaa, 0x3b, 0xaa, 0x3b, 0xba, 0x8e, 0xa8, 0xeb, 0xa3, 0xa8,
    0xaa, 0x28, 0xbb, 0xb8, 0xae, 0x2a, 0xe2, 0xee, 0x3a, 0xb8,
    0x00
]

def getValue(val):
    iVar2 = val
    if (val < 0):
        iVar2 = val + 7

    bVar1 = val >> 0x37
    return secret[iVar2 >> 3] >> (7 - ((val + (bVar1 >> 5) & 7) - (bVar1 >> 5)) & 0x1f) & 1

def encode():
    for character in characters:
        c = ord(character)
        if (c == ord(' ')):
            c = -0x7b
        elif (ord('0') <= c) and (c <= ord('9')):
            c += ord('K')

        c -= 0x61

        if (c != ord('$')):
            iVar2 = (c + 0x12) % 0x24
            bVar1 = (iVar2 >> 0x1f)
            c = (iVar2 ^ bVar1) - bVar1

        decoded_value = ""

        # Removed the `* 4` since that effectively selects every 4th byte.
        # Removing this also means we have to use the `pcw @ obj.indexTable` (C words, 4 byte)
        # representation instead of `pc @ obj.indexTable` (1 byte).
        index = indexTable[c]# * 4]
        end = indexTable[(c + 1)]# * 4]

        for i in range(index, end):
            decoded_value += str(getValue(i))

        print(str(character) + ": " + decoded_value)
        decoded_dict[decoded_value] = character


characters = string.ascii_lowercase + string.digits
decoded_dict = {}
encode()

print("Python dictionary: " + str(decoded_dict))