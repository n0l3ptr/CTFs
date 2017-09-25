# coding: utf-8
d = open('strings.txt', 'r').read()
lines = d[d.index('65535')+1:d.index('trailer')].split('\n')
print ''.join([chr(int(y, 16)) for y in [x.split()[1][3:] for x in lines if len(x) > 0] if y != '00' and y != ''][::-1])
