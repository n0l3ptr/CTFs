# BB8 Write-up (Crypto 200)

### Gathering tools
Going into this question, we had no knowledge of quantum crypto - [the wikipedia article](https://en.wikipedia.org/wiki/BB84) and [this youtube video](https://www.youtube.com/watch?v=UVzRbU6y7Ks) were a good intro for this question.

Once we had a decent idea of what was going on with the protocol, we nc to the server and see that we are able to intercept or not intercept qubits. If this was a classical data stream, all we would have to do is intercept the bits and forward them on; however, we can't do that here because intercepting qubits and measuring them changes their value. This means that when we intercept a qubit and forward on what we measured, we can't be certain this is an identical qubit to what we received.

![tcp interface with MitM server](https://github.com/n0l3ptr/Plaid2017/raw/master/pictures/Selection_192.png)

At this point we started coding the python script that would interact with the server. The first goal was to make a program that could get to the end of the communications. All this program would do is forward packets until both sides of the connection dropped (hopefully after they had sent their classical message).

The next goal was to make a function that would allow the script to intercept a single packet at any given point and optionally forward on what the measured value was. After that, we could really start working on the problem.

### Our solve part 1 - Alice's message to Bob

At this point we had all the tools we needed to start solving the question. We weren't 100% sure what the point of the question was yet, but had the tools and knowhow to pretend to be Bob through a MitM attack. So following the BB84 protocol, when Alice sent Bob a qubit, we measured it - always in basis Z, just to simplify things. Although this changed it when we sent it to Bob, we don't really care what he is thinking or doing [at the moment] and just forward on his Ack to Alice, which is always in basis Z, so it's ok to measure (but since this will always be 1 at this point in the protocol, it doesn't matter, and we save time by not intercepting.) This step ends after 1199 qubits have been sent (it isn't 1200 because Bob doesn't send an Ack for the last bit).

The next part of the protocol involves Bob sending the basises that he used to measure each respective qubit in Alice's key. So when he sends these to Alice, we intercept those and send a qubit indicating that 'Bob' measured in the Z axis. Alice replies, telling 'Bob' whether he was correct or incorrect. We forward this on, knowing that Alice and Bob will have different keys, but *not* knowing what Bob thinks Alice's key is. After this step, which ends after 2399 qubits have been sent total, there is the check to see if there was somebody listening on the connection.

This part is the key - if we have done something wrong by now, Alice will drop the connection if our key values disagree. We create a list of the qubit values sent by Alice in the Z basis, and start intercepting Bob's qubits to Alice, replacing them with every other value from our list. Since our attack does produce values Alice agrees with, she won't drop the connection. Alice sends Bob Acks, which we forward.

If all has gone well by this point, and for us it has, Bob sends Alice a classical AES128-ECB encrypted message, then Alice sends Bob another AES128-ECB key. This is the part where we thought we would get in trouble, because Alice and Bob don't have the same key. We were hoping that the messages weren't B->A "Hey give me the flag" then A->B "here is the flag". This would require them both to have the same key while we had no idea how to implement such an attack. (Fortunately, we were able to successfully decrypt Alice's message to Bob)[https://github.com/n0l3ptr/Plaid2017/blob/master/BB8/a2bsolve.py]! [Note: The message from Bob will be nonsense, poor Bob :(]

![A valid message and key from Alice](https://github.com/n0l3ptr/Plaid2017/raw/master/pictures/Selection_193.png)

And decrypting with [aes.py](https://github.com/n0l3ptr/Plaid2017/blob/master/BB8/aes.py)...

![Decrypting with aes.py](https://raw.githubusercontent.com/n0l3ptr/Plaid2017/master/pictures/Selection_198.png)

w00t! Alice's message is independent from Bob's! Now we just need to get Bob's message to Alice.

### Our solve part 2 - Bob's message to Alice

Now we just need to simultaneously establish a key between us and Alice *and* us and Bob. We only need to make 2 changes to our code above. First, instead of forwarding the qubit from Alice to Bob in the first step, we create our own key by always sending the value '1' in the Y basis (this is the most convenient to program). Second, in the second step of the protocol, we save the intercepted value from Bob (the basis he measured in) and will take this to intercept Alice's qubit and forward on whether Bob was right or not.

This technically works, but because I didn't tune my script, it is possible for Alice's confirmations from step 3 to happen *before* Bob's, which means her message to Bob is sent - then my program crashes :(. To work around this problem, I ran my program in 4 different windows. [My results, from solve.py](https://github.com/n0l3ptr/Plaid2017/blob/master/BB8/solve.py):

![Message from Bob to Alice](https://github.com/n0l3ptr/Plaid2017/raw/master/pictures/Selection_195.png)

![Message from Alice to Bob](https://raw.githubusercontent.com/n0l3ptr/Plaid2017/master/pictures/Selection_196.png)

And then plopping the corresponding values into aes.py:

![Final result](https://raw.githubusercontent.com/n0l3ptr/Plaid2017/master/pictures/Selection_197.png)

### TL;DR

Step 1. Learn about BB84 - the quantum key distribution protocol

Step 2. Realize that without any form of auth, as a MitM attacker we can create a different key with both Alice and Bob

Step 3. Write a script that simultaneously creates a valid key between us and Alice, then us and Bob

Step 4. Run the script multiple times because it is super hacky

Step 5. Decrypt with AES-ECB and the key we used.

-Mitch
