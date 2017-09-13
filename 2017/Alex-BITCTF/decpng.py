fn = "BITSCTFfullhd.png"
fn2 = "CyberSecurityClubFullResolution (1).png"
known = (0x72,0x6b,0x68,0x25,0x51,0x50,0x8e,0x67)

"""
for e in [0x72,0x6b,0x68,0x25,0x51,0x50,0x8e,0x67]:
	print chr(e)
"""

f = open(fn, 'r').read()
f2 = open(fn2, 'r').read(24)

known = [ord(c) for c in f2]

key = [x^ord(y) for x,y in zip(known,f)]#need to check these bits 18,19,22,23


#print key	

last24 = [x^ord(y) for x,y in zip(key*999999,f)][-24%len(f):]
#we know padding is 19 from last24

print last24
corrected6 = [0]*18+[x^19 for x in last24[-6%len(last24):]]

print corrected6

correctedkey = [x^y for x,y in zip(key,corrected6)]

print [hex(x) for x in correctedkey]

resstr = ""

#print "".join([chr(x^ord(y)) for x,y in zip(correctedkey*999999,f)])[:-19%len(f)]

