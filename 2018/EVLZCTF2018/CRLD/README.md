# CRLD - Create Read Link Delete (Pwn 500 pts)

We are given the following binary [crld_prog](./crld_prog). After running the file command I see it is a x86-64 executable. After running strings we find some interesting strings:

```
...
/home/crld/crld/
/home/crld/crld/flag
Timeout
Create-Read-Link-Delete Service
Base Path: %s
Commands:
	Create: create test hello_world
	Create Directory: create_dir test_dir
	Read: read test
	Link: link test test2
	Delete: delete test
Command:
...
```
This makes me believe the title is telling us exactly what the program is doing in that we have the option to Create, Read, Link, or Delete a file. At this point I thought this might be a race condition situation. Also, I noticed the string "/home/crld/crld" and "/home/crld/crld/flag" which meant our flag was probably in that directory and I probably needed to create the following directory "/home/crld/crld". At this point I ran strace next to confirm my suspicions.

```
chdir("/home/crld/crld/") = -1 ENOENT (No such file or directory)
```

Next I created the directory "/home/crld/crld" then I created a file called "flag" in that directory with the contents "FLAGFLAG". I then use the program to create a file called test with contents "dummy". While running the program with strace I tried to read  test and it printed out the contents. However, when I tried to read flag I got:

```
read(0, read flag
"read flag\n", 1024)            = 10
getcwd("/home/crld/crld", 4096)         = 16
lstat("/home/crld/crld/flag", {st_mode=S_IFREG|0664, st_size=9, ...}) = 0
access("/home/crld/crld/flag", F_OK)    = 0
write(1, "Illegal Operation", 17Illegal Operation)       = 17
```
Also, with ltrace I got the following:

```
strlen("/home/crld/crld")                                                                                                      = 15
strlen("flag")                                                                                                                 = 4
memcpy(0x7fff2e7e77f0, "flag", 4)                                                                                              = 0x7fff2e7e77f0
strchr("flag", '/')                                                                                                            = nil
memcpy(0x7fff2e7e87f0, "flag", 4)                                                                                              = 0x7fff2e7e87f0
strcmp("flag", ".")                                                                                                            = 56
strcmp("flag", "..")                                                                                                           = 56
strlen("/home/crld/crld/")                                                                                                     = 16
strlen("flag")                                                                                                                 = 4
memcpy(0x7fff2e7ea920, "flag", 4)                                                                                              = 0x7fff2e7ea920
__lxstat(1, "/home/crld/crld/flag", 0x7fff2e7e7760)                                                                            = 0
access("/home/crld/crld/flag", 0)                                                                                              = 0
strlen("/home/crld/crld/")                                                                                                     = 16
strncmp("/home/crld/crld/flag", "/home/crld/crld/", 16)                                                                        = 0
strcmp("/home/crld/crld/flag", "/home/crld/crld/flag")                                                                         = 0
puts("Illegal Operation"Illegal Operation
)      
```
With this I knew there was a comparison to check if we were trying to read the "/home/crld/crld/flag" file. Running ltrace with a different file "/home/crld/crld/test".

```
strncmp("/home/crld/crld/test", "/home/crld/crld/", 16)                                                                        = 0
strcmp("/home/crld/crld/test", "/home/crld/crld/flag")                                                                         = 14
__errno_location()                                                                                                             = 0x7fc1e4694698
getcwd(0x7fffd77d3bd0, 4096)                                                                                                   = "/home/crld/crld"
strlen("/home/crld/crld")                                                                                                      = 15
strlen("test")                                                                                                                 = 4
memcpy(0x7fffd77d0ab0, "test", 4)                                                                                              = 0x7fffd77d0ab0
strchr("test", '/')                                                                                                            = nil
memcpy(0x7fffd77d1ab0, "test", 4)                                                                                              = 0x7fffd77d1ab0
strcmp("test", ".")                                                                                                            = 70
strcmp("test", "..")                                                                                                           = 70
strlen("/home/crld/crld/")                                                                                                     = 16
strlen("test")                                                                                                                 = 4
memcpy(0x7fffd77d3be0, "test", 4)                                                                                              = 0x7fffd77d3be0
__lxstat(1, "/home/crld/crld/test", 0x7fffd77d0a20)                                                                            = 0
open("/home/crld/crld/test", 0, 023)                                                                                           = 3

```
I noticed the string comparison happens before the a call to open. Furthermore the file I was trying to read, its full path was recalculated after the check for flag. I further tested the binary to see if I could create a link to the flag file and then read it's contents but that did not pass the flag file check either. At this point I decided this was a race condition challenge. I needed a call to read to happen such that when the comparison for flag happened a legitimate file not name flag was in existence and before the call to open I needed that same file to be changed to a link to the flag file. So I crafted the exploit found in [solve.py](./solve.py). Running this on my local machine produced the contents of the flag file most of the time. So I then tried it on the remote machine. It took a couple of tries but I finally was able to get the flag to print.
