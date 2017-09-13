import commands
import socket
import time
import sys
from threading import Thread

host = "195.154.53.62"
port = 7412

socketarray = []
threadarray = []

for x in xrange(0,50):
 s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 socketarray.append(s)

def connect_socket(x):
  x.connect((host,port))

for x in socketarray:
  t = Thread(target=connect_socket, args=(x,))
  threadarray.append(t)

for x in threadarray:
  x.start()

for x in threadarray:
  x.join()

print "Done. Threads ready:"
print len(socketarray)

def handle_sync(s1, s2):
  s_in_use = s1
  inp = ""
  while True:
    while inp != "switch":
      inp=raw_input("> ")
      if inp == "switch":
        continue
      else:
        s_in_use.send(inp+"\n")
        print s_in_use.recv(1024)
    if s_in_use == s1:
      s_in_use = s2
    else:
      s_in_use = s1
    print "Switched"
    inp = ""

s_dict = {}
print "Beginning.."
initial = None
readysockets = []
for x in socketarray:
  init_resp=x.recv(1024)
  x.send("2\n")
  resp=x.recv(1024)
  clock=resp.splitlines()[0]
  if clock not in s_dict.keys():
    s_dict[clock] = x
  else:
    print "Got a synchronized socket"
    handle_sync(x, s_dict[clock])
  if initial is None:
    initial=clock
  if clock == initial:
    readysockets.append(x)
