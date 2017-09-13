import base64
f = open('img.bmp', 'rb')
d = f.read()
v = d[0x7a:] #skip the header
u = ''.join([base64.b64decode(x) for x in v.split('\n')])
open('img.out', 'wb').write(u)
