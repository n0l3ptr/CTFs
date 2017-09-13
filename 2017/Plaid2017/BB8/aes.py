#helper script for BB84
#wanted to make this independent of the solve script
from Crypto.Cipher import AES

#bob's will be constant, alice's will vary
bobKey = ['1']*128
aliceKey = ['-1', '-1', '1', '1', '-1', '-1', '-1', '-1', '-1', '-1', '1', '-1', '1', '1', '-1', '1', '-1', '-1', '-1', '1', '1', '-1', '-1', '1', '-1', '-1', '1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '1', '1', '1', '1', '-1', '-1', '1', '1', '1', '-1', '1', '1', '-1', '-1', '-1', '1', '-1', '1', '1', '1', '1', '1', '-1', '-1', '1', '1', '-1', '1', '1', '1', '1', '-1', '-1', '1', '-1', '1', '-1', '1', '1', '-1', '-1', '1', '-1', '-1', '1', '1', '-1', '1', '1', '-1', '1', '-1', '1', '1', '1', '-1', '1', '-1', '1', '1', '-1', '-1', '-1', '1', '-1', '1', '1', '1', '1', '-1', '-1', '1', '-1', '1', '-1', '-1', '1', '-1', '1', '1', '-1', '1', '-1', '-1', '-1', '-1', '1', '1', '-1', '1', '1', '1', '-1', '1', '1', '1', '1', '-1', '-1', '1', '-1', '-1', '1', '-1', '1', '-1', '-1', '1', '1', '1', '-1', '-1', '-1', '-1', '1']

msgA2B = 'c30c41c25e42fd99598e6dd764468ccbb2445cb4f29c58c89814c5043af7f16c'
msgB2A = '80dc59ce81e30bcd02198059b556731597ce5cf597481229ac9b2d523516c83e0f65896ce3b51cc2eb5b120adca55ed8'

def decrypt(msg, keylist):
    #it'd be embarrassing if there were an easier way to convert this
    #'1'  -> 1
    #'-1' -> 0
    key = "".join([('1','0')[val=='-1'] for val in keylist[:128]])

    #now convert binary list to ascii
    key = "".join([chr(int(key[i:i+8],2)) for i in range(0,len(key),8)])

    iv = ""
    msg = msg.decode('hex')

    #decrypt
    cipher = AES.new(key,AES.MODE_ECB,iv)

    return cipher.decrypt(msg)

print decrypt(msgA2B, aliceKey).strip()+decrypt(msgB2A, bobKey).strip()
