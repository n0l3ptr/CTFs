
#get the range of libc
a =  [s.split() for s in peda.execute_redirect('info proc mapping').split('\n') if 'libc' in s]
rang = (int(a[0][0], 16), int(a[-1][1], 16))
print ("rang = (base, end) = ", rang)

#search the stack for addresses within rang^^
def search_stack():
    tupls = [t for t in [(a[0]-3, struct.unpack("<Q", peda.readmem(a[0]-3, 8))[0]) for a in peda.searchmem(peda.getreg("rsp"), peda.get_vmmap("stack")[0][1], str(hex(rang[0]))[0:8])] if t[1] in range(rang[0], rang[1])]
    print (''.join([ str(hex(x[1] - rang[0]))  + ' ' + str(hex(x[0])) + " ---> " + peda.get_disasm(x[1])  + '\n' for x in tupls]))
    return tupls

#provide the libc range the address on the stack you want to find the offset from and the number of bytes per offset 
def find_stack_offset_from(tupls, addr, b):
    for t in tupls:
        off = (t[0] - addr) / b
        print (''.join(str(int(off)) + ' ' + str(hex(t[1] - rang[0]))  + ' ' + str(hex(t[0])) + " ---> " + peda.get_disasm(t[1])  + '\n'))
