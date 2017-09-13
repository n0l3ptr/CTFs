# PPLC (Programming)
### Tokyo Western CTF 2017

```
yet another PLC challange as last year's?

private: nc ppc1.chal.ctf.westerns.tokyo 10000
local: nc ppc1.chal.ctf.westerns.tokyo 10001
comment: nc ppc1.chal.ctf.westerns.tokyo 10002

restricted_python.7z

Note: If you cannot connect the server with nc command, please try ncat command(included nmap package).
```

[restricted_python.7z](restricted.7z)

#### Private
```
import sys
from restrict import Restrict

r = Restrict()
# r.set_timeout()

class Private:
    def __init__(self):
        pass

    def __flag(self):
        return "TWCTF{CENSORED}"

p = Private()
Private = None

d = sys.stdin.read()
assert d is not None
assert "Private" not in d, "Private found!"
d = d[:24]

r.seccomp()

print eval(d)

```
In order to solve this I needed to print out the "private" function 'flag' but Private is set to None so all I have is an instance of the class. My input cannot contain Private so p._Private__flag() won't work. Also, it can only be 24 bytes. So I was able to get it with the following:
```
 eval("p.%s()"%dir(p)[0])
```

TWCTF{__private is not private}

#### Local
```
import sys
from restrict import Restrict

r = Restrict()
# r.set_timeout()

def get_flag(x):
    flag = "TWCTF{CENSORED}"
    return x

d = sys.stdin.read()
assert d is not None
d = d[:30]

r.seccomp()

print eval(d)

```
Not to restricted here. We just have to keep it to 30 bytes. The following did the trick.

```
get_flag.func_code.co_consts
```
TWCTF{func_code is useful for metaprogramming}

#### Comment

##### comment.py
```
import sys
from restrict import Restrict

r = Restrict()
# r.set_timeout()

d = sys.stdin.read()
assert d is not None
d = d[:20]

import comment_flag
r.seccomp()

print eval(d)
```

##### comment_flag.py
```
'''
Welcome to unreadable area!
FLAG is TWCTF{CENSORED}
'''
```
For this one we just need to be able to read the code from an imported module. The following solved this problem.

```
comment_flag.__doc__
```
TWCTF{very simple docstring}
