# Rusted From The Rain (REV 200)

```
Some conspiracy theorists like to claim Earth is actually flat and surrounded by an ice wall guarded by the Night's Watch NASA employees. Seriously though, only fools would believe that! The real conspiracy goes much deeper, they want to shield the remains of highly advanced ancient civilizations from us but we were able to obtain an old data storage device! It appears they left us a message, however thousands of years of exposure to the elements took their toll and we couldn't extract anything but a tool that was apparently used to verify the message. Can you help us recover the message?
```
[file](ctf_normie_cpu-14f48b9bc8ff3d1d.exe)

(TODO BETTER WRITEUP)

#### Initial
* Run file command to see it is a PE file
* Run strings and notice interesting string "Yep, congrats.Try again."
* Run program and realize we must pass the flag as an arguments
* Angr seems like a good thing to try...

#### Reversing
* Find xrefs to string "Yep, congrats.Try again."
* Notice cmovnz that determines whether we get congrats or try again
* Notice return from previous function needs to be non-zero
* Use debugger to see arguments to function call are len(argv[1]) and argv[1].
* Analyze the beginning of the "checkFlag" function to see the size must be equal to 0x1c or 28 bytes and that the first four chars are FLAG
* Note where the function set $rax to 1.

#### Angr Steps:

* Create angr state at location of call to checkFlag()
* Set up int size and char* flag arguments to checkFlag()
* Find path to location in checkFlag where 1 will be returned
* Print symbolic memory of flag with found path's state's symbolic engine
