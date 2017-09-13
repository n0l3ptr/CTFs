# coding: utf-8
import itertools
import hashlib
from subprocess import Popen, PIPE

list1 = itertools.product('0123456789abcdefABCDEF', repeat=4)
potentials = []
for e in list1:
    res = hashlib.sha1(''.join(e)).hexdigest()
    if res.startswith(''.join(e)):
        potentials.append(''.join(e))
        print "Found {},{}".format(''.join(e), res)


x1 = int(potentials[0], 16)
x2 = int(potentials[1], 16)
part1 = ""
part3 = ""
if x2 < x1:
    part3 = potentials[0]
    part1 = potentials[1]
else:
    part1 = potentials[0]
    part3 = potentials[1]

part2_a = part1[-1]
part2_b = part3[0]

print "Guessing: {}????{}".format(part2_a, part2_b)

i = 0
ans = '69fc8b9b1cdfe47e6b51a6804fc1dbddba1ea1d9'
#list = itertools.product('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-]+.', repeat=4)
import string
list = itertools.product(string.printable, repeat=4)
for e in list:
    i+=1
    res = part2_a + ''.join(e) + part2_b
    '''
    process = Popen(["./abc", res], stdout=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()
    print res
    if "Sorry" not in output:
        print "Found {}".format(res)
        break
    '''
    d = hashlib.sha1(res).hexdigest()
    print res
    if d == ans:
        print "Found: {}".format(part1 + ''.join(e) + part2)
        break
    
