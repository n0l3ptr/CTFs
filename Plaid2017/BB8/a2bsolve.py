#client to solve quantum cryptography
#WARNING: Very hacky and unoptimized
#First version of the script that only gets Alice's key and classical message
#Not permitted for use in hacking real-world BB84 or BB-8

from pwn import *
import sys

r = remote("bb8.chal.pwning.xxx", 20811)
key2bob = b'0'*600
bobacks = []
aliceinterp = []#the bits from alice interpreted in z basis
correctlist = []#the bits from alice which we interpreted correctly

def intercept(b, val='1', p='N', nb='Z'):
    #intercept
    r.sendline('Y\n{}\n{}'.format(b, p))
    d = r.recvline()
    #print 'a', d

    #send in basis b
    #r.sendline(b)
    d = r.recvline()
    #print 'b', d
    #print d.split(' ')
    res = d.split(' ')[2]
    d = r.recvline()
    #print 'e', d

    #replace N/Y, default is no
    #r.sendline(p)
    d = r.recvline()
    #print 'c', d
    if p.lower() == 'n':
        d = r.recvline()
        #print 'd', d

    else:
        #we are intercepting
        r.sendline(nb+'\n'+val)
        d = r.recvline()
        #print 'd', d

        d = r.recvline()
        #print 'f', d

    return res.strip()

def keyexchange():
    print "exchanging keys"
    d = r.recvline()
    print d
    for i in range(599):
        #this corresponds to a bit of alice's key to Bob
        #r.sendline()
        #d = r.recvline()
        #print d
        inter = intercept('Z')
        aliceinterp.append(inter)

        #bob's ack
        r.sendline()
        d = r.recvline()
        print d
        #bobacks.append(intercept('Z', '1'))
        print i

    #this is alice's last bit sent to bob from the key
    inter = intercept('Z')
    aliceinterp.append(inter)

def guessexchange():
    print "Exchanging guesses\n"

    for i in range(600):
        #this is bob's guess for the basis of the ith key
        #injecting our guess instead
        intercept('z', val='-1', p='Y', nb='Z')

        #this corresponds to alice teling bob if he was correct
        #we are reading correct/not, but we don't care about sending it on
        correctlist.append(intercept('z', p='n'))
        print i, i

    #this is alice's last bit sent to bob from the key
    print correctlist
    print aliceinterp

    return [aliceinterp[i] for i in range(600) if correctlist[i] =='1']

def listenexchange(bases):
    print "Exchanging info to see if someone was listening to the connection\n"

    for i in range(len(bases)):
        if i % 2 == 1:
            continue

        #intercept message from bob to alice
        #give alice our value instead
        intercept('z', val=bases[i], p='Y', nb='Z')

        #alice sends acks now, we dgaf
        r.sendline()
        d = r.recvline()
        print d
        print i, i, i

    print [i for j,i in enumerate(bases) if j % 2 == 1]

    #this is alice's last bit sent to bob from the key
    r.sendline()
    d = r.recvline()
    print d
    r.sendline()
    d = r.recvline()
    print d
    r.sendline()
    d = r.recvline()
    print d

def messageexchange():
    #this should be the aes message by now
    pass

if __name__ == "__main__":
    print "Starting"

    d = r.recvuntil('good luck...\n')
    print d

    keyexch = keyexchange()
    bases = guessexchange()
    listening = listenexchange(bases)
    msg = messageexchange()
    print bobacks

"""
Alice and Bob are communicating with their fancy new QKD devices. Their protocol is fairly standard, but we've
learned enough details to be worth reporting.

Alice generates 600 qubits, each with a random (Y or Z) basis and (-1 or 1) value. Alice sends each of these
qubits to Bob, who acknowledges their receipt with a 1 in the Z basis.

As soon as Bob receives the 600th qubit, he begins to transmit his guessed bases to Alice. He sends these via the
Z basis, with -1 corresponding to a Z, and a 1 corresponding to a Y. After each guess, Alice will tell Bob if the guess
was in the correct basis or not (a 1 in the Z basis means correct, a -1 means wrong).

As soon as Bob finishes these transmissions, Alice and Bob make sure no one was listening to their exchange. Bob
takes every other measurement he made where Alice verified the basis as correct (so he takes the 0th agreed value, the
2nd agreed value, 4th, and so on). He sends the values he measured on these positions to Alice using the Z basis.
If Alice disagrees with any of the value sent, this means an eavesdropper was on the line, and she immediately aborts.
Otherwise, she sends Bob an ACK in the form of a 1 in the Z basis.

After this phase has completed, Alice and Bob trust that there was not an eavesdropper present on the line. They use
the first 128 agreed measurements which were not already spent (so the 1st, 3rd, 5th, and so on agreed values) to
establish a shared AES key (the 128 values are treated as as 128bit binary key, -1 corresponding to 0, and 1 to 1)
If there are not 128 unused values on which Alice and Bob agree on the bases, then the connection is aborted.

Finally, Alice and Bob each send their 200% secure AES128-ECB encrypted message!
"""
