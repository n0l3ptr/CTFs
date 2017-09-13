import base64

l = [str(1*(x.strip()=="ONE")) for x in open("zero_one", 'r').read().split(' ')]

print "".join(l)

m = "".join([chr(int("".join(l[i*8:i*8+8]),2)) for i in range(len(l)/8)])

print m

print base64.b64decode(m)
