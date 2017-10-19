# coding: utf-8
import angr
p = angr.Project('./ctf_normie_cpu-14f48b9bc8ff3d1d.exe', load_options={'auto_load_libs' : False})
offset = 0x140019328-0x13FF19328
init = p.factory.blank_state(addr=0x13ff0172c+offset)
len_pwd = 0x1c
init.regs.rdx = len_pwd
init.regs.rcx = 0x60000
pw = init.se.BVS('pw', 8*0x1c)
init.add_constraints(pw.get_bytes(0,4) == "FLAG")
init.memory.store(0x60000, pw)
pg = p.factory.path_group(init, immutable=False)
pg.explore(find=0x13ff0131d+offset)
if len(pg.found) > 0:
    print pg.found[0].state.se.any_str(pw)
