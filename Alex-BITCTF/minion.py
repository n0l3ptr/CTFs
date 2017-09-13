import string

fn = "MinionQuest.pdf"

lc = string.lowercase*2
uc = string.uppercase*2

fstring = ""

flist = [c for c in open(fn, 'r').read()]
print flist

for c in flist:
	if c in lc:
		c = lc[lc.index(c)+13]
	if c in uc:
		c = uc[uc.index(c)+13]
	fstring += c
		
with open(fn+".res", 'w') as f:
	f.write(fstring)
