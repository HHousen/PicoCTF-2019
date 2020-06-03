data_1 = bytearray.fromhex('43467b416e315f38353536313164337d')
data_2 = bytearray.fromhex('8573')
data_3 = bytearray.fromhex('696354307468615f')

flag = bytearray(b'0'*0x1a)

flag[1] = data_3[0]
flag[0] = data_2[0] - 0x15
flag[2] = data_3[1]
flag[5] = data_3[2]
flag[4] = data_1[0]

for i in range(6,10):
  flag[i] = data_1[i-5] # have retrieved 1 byte so far from this file

flag[3] = data_2[1]-4

for i in range(10, 15):
  flag[i] = data_3[i-7] # have retrieved 3 bytes so far from this file

for i in range(15,26):
  flag[i] = data_1[i-10] # have retrieved 5 bytes so far from this file

print("Flag: {}".format(flag.decode('ascii')))
