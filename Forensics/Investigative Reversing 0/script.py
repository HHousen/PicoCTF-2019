data = bytearray.fromhex('7069636f43544b806b357a73696436715f35323636613835377d')

for i in range(6, 15):
  data[i] -= 5 # subtract 5 since 5 was added initially

data[15] += 3 # add 3 since 3 was subtracted initially

print("Flag: {}".format(data.decode('ascii')))
