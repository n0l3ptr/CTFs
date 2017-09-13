import angr, claripy, r2pipe, re, sys, struct, subprocess
import IPython
import os
import time

def getMainAddr(p):
    addr = 0
    entry = p.entry
    r2 = r2pipe.open(p.filename)
    r2.cmd('aaa')
    s = r2.cmd('afl')
    addr = int([l.split()[0] for l in s.split('\n') if 'main' in l and 'libc' not in l][0], 16)
    return addr
def getMainAddr2(cfg):
    for address,function in cfg.functions.iteritems():
        if 'printf' in function.name:
            addr = cfg.functions.callgraph.predecessors(address)[0]
            return addr
                                                        
def static_analysis(p):
    to_find, to_avoid, byte_addresses = [], [], []
    find_hex_re = re.compile('(0x[0-9a-fA-F]{6})')
    cfg = p.analyses.CFGFast()
    addr = getMainAddr3(p)
    while True:
        function = cfg.functions.function(addr)
        call_sites = function.get_call_sites()
        if not len(call_sites):
            break
        #Now, Let's get the address of the basic block calling the next target function.
        #The sorting and indexing is only relevant for the main function.
        avoid_addr = sorted(call_sites)[-1]
        find_addr = sorted(call_sites)[-2]
        to_find.append(find_addr)
        to_avoid.append(avoid_addr)
        return to_find, to_avoid
def static_analysis2(p):
    to_find, to_avoid, byte_addresses = [], [], []
    find_hex_re = re.compile('(0x[0-9a-fA-F]{6})')
    cfg = p.analyses.CFGFast()
    addr = getMainAddr2(cfg)
    while True:
        function = cfg.functions.function(addr)
        call_sites = function.get_call_sites()
        if not len(call_sites):
            break
        #Now, Let's get the address of the basic block calling the next target function.
        #The sorting and indexing is only relevant for the main function.
        avoid_addr = sorted(call_sites)[-1]
        find_addr = sorted(call_sites)[-2]
        to_find.append(find_addr)
        to_avoid.append(avoid_addr)
        return to_find, to_avoid

def main():
    f = open('results', 'wa')
    for p in os.listdir('./'):
        if 'prob' not in p:
            continue
        proj = angr.Project('./' + p, load_options={"auto_load_libs": False})
        argv1 = angr.claripy.BVS("argv1", 40 * 8)
        start = time.time()
        to_find, to_avoid = static_analysis(proj)
        end = time.time()
        print "Static analysis 1 Completed In: %f" % (end-start)
        start = time.time()
        to_find, to_avoid = static_analysis2(proj)
        end = time.time()
        print "Static analysis 2 Completed In: %f" % (end-start)
        
        initial_state = proj.factory.entry_state(args=["./prob1", argv1])
        initial_path = proj.factory.path(initial_state)
        path_group = proj.factory.path_group(initial_state)
        path_group.explore(find=to_find, avoid=to_avoid)
        found = path_group.found[0]
        s = p[4:] + ' = ' + found.state.se.any_str(argv1) + '\n'
        f.write(s)
        print s

def test():
    res = main()
    print repr(res)
    

if __name__ == '__main__':
    main()
