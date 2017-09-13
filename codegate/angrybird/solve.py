import subprocess
import angr
from claripy import BVS, Or, And
import simuvex

#auto_load_libs option is set to false which tells the loader to not automatically load
#requested libraries. This is so angr doesn't analyze paths in shared libraries
p = angr.Project("angrybird", load_options={'auto_load_libs' : False})

firstfind = 0x400778 #set eax to 1 and continue
secondfind = 0x4007ab #set eax to 21
thirdfind = 0x40071e #set eax to 0, store "hello" at 0x606038
fourthfind = 0x4007c2 # now we are up to stdin must be 21 bytes

init = p.factory.entry_state()

print ("Exploring..")
#speeds up angr quite a bit
init.options.discard("LAZY_SOLVES")

pg = p.factory.path_group(init, immutable=False)
pg.explore(find=firstfind)
s = pg.found[0].state
s.regs.rax = 0x1
pg = p.factory.path_group(s, immutable=False)
pg.explore(find=secondfind)
s = pg.found[0].state
s.regs.rax = 21
pg = p.factory.path_group(s, immutable=False)
pg.explore(find=thirdfind)
s = pg.found[0].state
s.regs.rax = 0
s.memory.store(0x606038, "hello")
pg = p.factory.path_group(s, immutable=False)
pg.explore(find=fourthfind)
s = pg.found[0].state

#avoid function
def incorrect(path):
    try:
        return 'melong' in path.state.posix.dumps(1)
    except:
        False

#set up stdin
# Constrain the first 20 bytes to be non-null and non-newline:
for _ in xrange(20):
    k = s.posix.files[0].read_from(1)
    s.se.add(k != 0)
    s.se.add(k != 10)
    
# Constrain the last byte to be a newline
k = s.posix.files[0].read_from(1)
s.se.add(k == 10)

# Reset the symbolic stdin's properties and set its length.
s.posix.files[0].seek(0)
s.posix.files[0].length = 21

pg = p.factory.path_group(s, immutable=False)
pg.explore(avoid=incorrect)
#the flag should be in a deadended path
for p in pg.deadended:
    print p.state.posix.dumps(1)
