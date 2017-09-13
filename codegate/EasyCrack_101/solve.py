import angr, claripy
import os
def getMainAddr(cfg):
    #I guessed printf would be in main for every binary after looking at the first three
    for address,function in cfg.functions.iteritems():
        if 'printf' in function.name:
            addr = cfg.functions.callgraph.predecessors(address)[0]
            return addr
    
def static_analysis(p):
    to_find, to_avoid = [], []
    cfg = p.analyses.CFGFast()
    addr = getMainAddr(cfg)
    function = cfg.functions.function(addr)
    call_sites = function.get_call_sites()
    if not len(call_sites):
        return None, None
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
        argv1 = claripy.BVS("argv1", 40 * 8) #the key is probably less than 40 bytes
        to_find, to_avoid = static_analysis(proj)
        initial_state = proj.factory.entry_state(args=["./prob1", argv1])
        initial_path = proj.factory.path(initial_state)
        path_group = proj.factory.path_group(initial_state)
        path_group.explore(find=to_find, avoid=to_avoid)
        found = path_group.found[0]
        s = p[4:] + ' = ' + found.state.se.any_str(argv1) + '\n'
        s = s.replace('\x00', '')
        f.write(s)
        print s

if __name__ == '__main__':
    main()
