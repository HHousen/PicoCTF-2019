#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 2019shell1.picoctf.com --user xxx --pass 'xxx' --path /problems/time-s-up_1_7d4f79c3df3e1b044801573eea5722be/times-up
from pwn import *
import sys

# Set up pwntools for the correct architecture
# ELF tutorial: https://github.com/Gallopsled/pwntools-tutorial/blob/master/elf.md
exe = context.binary = ELF('times-up')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '2019shell1.picoctf.com'
port = int(args.PORT or 22)
user = args.USER
password = args.PASSWORD
remote_path = '/problems/time-s-up_1_7d4f79c3df3e1b044801573eea5722be/times-up'
remote_dir = '/problems/time-s-up_1_7d4f79c3df3e1b044801573eea5722be'

# Connect to the remote SSH server
shell = None
if not args.LOCAL:
    shell = ssh(user, host, port, password)
    shell.set_working_directory(symlink=True)

def local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

def remote(argv=[], *a, **kw):
    '''Execute the target binary on the remote host'''
    if args.GDB:
        return gdb.debug([remote_path] + argv, gdbscript=gdbscript, ssh=shell, *a, **kw)
    else:
        # `cwd` is needed here because the `vuln` executable does not use absolute paths, so we
        # must be in the folder that contains the flag.
        return shell.process([remote_path] + argv, cwd=remote_dir, *a, **kw)

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.LOCAL:
        return local(argv, *a, **kw)
    else:
        return remote(argv, *a, **kw)

io = start()

io.recvuntil("Challenge: ")
challenge = io.recvline()
answer = eval(challenge)
io.sendline(str(answer))
io.interactive()

# Script to paste on shell server:
# io = process("./times-up")
# io.recvuntil("Challenge: ")
# challenge = io.recvline()
# answer = eval(challenge)
# io.sendline(str(answer))
# io.interactive()