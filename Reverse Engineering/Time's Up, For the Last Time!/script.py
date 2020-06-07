#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pwntools config is first part of file. important code begins on line 58

# This exploit template was generated via:
# $ pwn template --host 2019shell1.picoctf.com --user xxx --pass 'xxx' --path /problems/time-s-up--for-the-last-time-_5_b2df97b433878873b16cff47337769d6/times-up-one-last-time
from pwn import *
import sys

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '2019shell1.picoctf.com'
port = int(args.PORT or 22)
user = args.USER
password = args.PASSWORD
remote_path = '/home/<username>/no_sigalrm'
remote_dir = '/problems/time-s-up--for-the-last-time-_5_b2df97b433878873b16cff47337769d6'

# Connect to the remote SSH server
shell = None
if not args.LOCAL:
    shell = ssh(user, host, port, password)
    shell.set_working_directory(symlink=True)

def local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug(["no_sigalrm"] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process(["no_sigalrm"] + argv, *a, **kw)

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


# New exploit code:
class Infix:
    def __init__(self, function):
        self.function = function
    def __ror__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __or__(self, other):
        return self.function(other)
    def __rlshift__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __rshift__(self, other):
        return self.function(other)
    def __call__(self, value1, value2):
        return self.function(value1, value2)

L = Infix(lambda x,y: x)
R = Infix(lambda x,y: y)

io = start()

io.recvuntil("Challenge: ")
challenge = str(io.recvline())

# Replace special operators with custom infix operators:
challenge = challenge.replace("f", "|L|")
challenge = challenge.replace("o", "|R|")
challenge = challenge.replace("r", "|R|")
challenge = challenge.replace("t", "|L|")
challenge = challenge.replace("x", "|R|")

answer = eval(challenge)
print("Answer: " + str(answer))
io.sendline(str(answer))
io.recvuntil("Congrats! Here is the flag!\n")
flag = io.recvuntil("}")
log.success(flag)
# io.interactive()
