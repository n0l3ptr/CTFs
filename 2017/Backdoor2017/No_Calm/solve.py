import angr, claripy


#avoid function
def incorrect(path):
        try:
            return 'not yet' in path.state.posix.dumps(1)
        except:
            return False
                        

proj = angr.Project('./challenge', load_options={"auto_load_libs": False})
argL = ["./challenge"]
for i in range(0, 0x1e):#the flag is 0x1d bytes
    argv = claripy.BVS("argv{}".format(i), 1 * 8) 
    argL.append(argv)
print len(argL)
initial_state = proj.factory.entry_state(args=argL)
initial_path = proj.factory.path(initial_state)
path_group = proj.factory.path_group(initial_state)
path_group.explore(avoid=incorrect)
found = path_group.deadended[0]
flag = ''
for a in argL[1:]:
    flag += found.state.se.any_str(a)
flag = flag.replace('\x00', '')
print flag

