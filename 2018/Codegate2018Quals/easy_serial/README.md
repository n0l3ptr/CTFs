## easy_serial (RE 350pts, 40 Solves)
The binary file:
[easy](./21ad6600a0045e8091c81706c6907d1d)


We are given a zip file, once we unzip it we have a 64 bit elf executable with the file name "easy". If we run strings on the binary we are given a lot of strings. I'd ignored that at first and ran the program to see what it gave me.
```
> ./easy
Input Serial Key >>>
hello
easy: Prelude.!!: index too large

```

I wasn't sure what Prelude. !!: index too large meant. So, I looked it up and realized this was a Haskell program that had been compiled. Having never used Haskell before I read about some of it's semantics and came across a Haskell decompilation tool called [hsdecomp](https://github.com/gereeter/hsdecomp). Rather than throw the binary in IDA or Radare I decided to give the decompiler a shot. I ran the decompiler and it did not work at first.

I eventually fixed the decompiler so that it would run if you would like to know how I did this see Appendix A. The output I was given is in the file [d.out](d.out). Rather than fixing the hsdecomp output internally I wrote a quick script in IPython to output the information as a strings rather than a set of tuples.
```
s = !cat d.out
for el in s:
    d = eval(el)
    res = ""
    for stat in d:
        res += stat + ' '
    print res
```
Then I was able to get [easy.hs](easy.hs), I then added some comments and it is pasted below:
```
Main_main_closure = >> $fMonadIO
    (putStrLn (unpackCString# "Input Serial Key >>> "))
    (>>= $fMonadIO
        getLine
        (\s1dZ_info_arg_0 ->
            >> $fMonadIO
                (putStrLn (++ (unpackCString# "your serial key >>> ") (++ s1b7_info (++ (unpackCString# "_") (++ s1b9_info (++ (unpackCString# "_") s1bb_info)))))) #Print out three chunks with _

###FIRST CHUNK COMPARISON
                (case && (== $fEqInt (ord (!! s1b7_info loc_7172456)) (I# 70)) #F
		(&& (== $fEqInt (ord (!! s1b7_info loc_7172472)) (I# 108)) #l
		(&& (== $fEqInt (ord (!! s1b7_info loc_7172488)) (I# 97))  #a
		(&& (== $fEqInt (ord (!! s1b7_info loc_7172504)) (I# 103)) #g
		(&& (== $fEqInt (ord (!! s1b7_info loc_7172520)) (I# 123)) #{
		(&& (== $fEqInt (ord (!! s1b7_info loc_7172536)) (I# 83))  #s
		(&& (== $fEqInt (ord (!! s1b7_info loc_7172552)) (I# 48))  #0
		(&& (== $fEqInt (ord (!! s1b7_info loc_7172568)) (I# 109)) #m
		(&& (== $fEqInt (ord (!! s1b7_info loc_7172584)) (I# 101)) #e
		(&& (== $fEqInt (ord (!! s1b7_info loc_7172600)) (I# 48))  #0
		(&& (== $fEqInt (ord (!! s1b7_info (I# 10))) (I# 102)) #f
		(&& (== $fEqInt (ord (!! s1b7_info (I# 11))) (I# 85)) #U
		(== $fEqInt (ord (!! s1b7_info (I# 12))) (I# 53))))))))))))) of #5
                    <tag 1> -> putStrLn (unpackCString# ":p"),

###SECOND CHUNK COMPARISON                    
		c1ni_info_case_tag_DEFAULT_arg_0@_DEFAULT -> case == ($fEq[] $fEqChar) (reverse s1b9_info)
		(: (C# 103) (: (C# 110) (: (C# 105) (: (C# 107) (: loc_7168872 (: loc_7168872 (: (C# 76) (: (C# 51)
    (: (C# 114) (: (C# 52) [])))))))))) of #gnik00L3r4
                        False -> putStrLn (unpackCString# ":p"),

##THIRD CHUNK COMPARISON (s1bb_info == our third chunk, !! s1bb_info loc_7172456 is first char in our chunk)
                        True -> case &&
		(== $fEqChar (!! s1bb_info loc_7172456) (!! s1b3_info loc_7172456)) #A
		(&& (== $fEqChar (!! s1bb_info loc_7172472) (!! s1b4_info (I# 19))) #t
		(&& (== $fEqChar (!! s1bb_info loc_7172488) (!! s1b3_info (I# 19))) #T
		(&& (== $fEqChar (!! s1bb_info loc_7172504) (!! s1b4_info loc_7172568)) #h
		(&& (== $fEqChar (!! s1bb_info loc_7172520) (!! s1b2_info loc_7172488)) #3
		(&& (== $fEqChar (!! s1bb_info loc_7172536) (!! s1b3_info (I# 18))) #S
		(&& (== $fEqChar (!! s1bb_info loc_7172552) (!! s1b4_info (I# 19))) #t
		(&& (== $fEqChar (!! s1bb_info loc_7172568) (!! s1b2_info loc_7172504)) #4
		(&& (== $fEqChar (!! s1bb_info loc_7172584) (!! s1b4_info (I# 17))) #r
		(== $fEqChar (!! s1bb_info loc_7172600) (!! s1b4_info (I# 18))))))))))) of #s
                            <tag 1> -> putStrLn (unpackCString# ":p"),
                            c1tb_info_case_tag_DEFAULT_arg_0@_DEFAULT -> putStrLn (unpackCString# "Correct Serial Key! Auth Flag!")
                )
        )
    )

s1b4_info = unpackCString# "abcdefghijklmnopqrstuvwxyz"
loc_7172600 = I# 9
s1bb_info = !! s1b5_info loc_7172488 #our third chunk of input
loc_7172488 = I# 2
s1b5_info = splitOn $fEqChar (unpackCString# "#") s1dZ_info_arg_0 #split our input on '#'
loc_7172584 = I# 8
loc_7172504 = I# 3
s1b2_info = unpackCString# "1234567890"
loc_7172568 = I# 7
loc_7172552 = I# 6
s1b3_info = unpackCString# "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
loc_7172536 = I# 5
loc_7172520 = I# 4
loc_7172472 = I# 1
loc_7172456 = I# 0
loc_7168872 = C# 48
s1b9_info = !! s1b5_info loc_7172472 #our second chunk of input
s1b7_info = !! s1b5_info loc_7172456 #our 0th or first chunk of input

```

I realized this wasn't working code but it was somewhat easy to read once I read up on some Haskell syntax. The biggest revelation being that !! is how you access an array element in Haskell. I determined that my input was being split based on a '#' sign and then printed with the pound sign replaced by '\_'. Then I recognized three If equal statements. The first two were pretty easy to read. The first one simply checked the first chunk of our split input to see if it equaled: Flag{S0me0fU5. It did this by comparing each ordinal value of each char in my first chunk with certain integers. The second statement did the same thing but it reversed the string 4r3L00king. The last statement indexed into the strings located at the bottom of the script. I chose to go through this by hand and see what it was comparing our input to. It turned out to be AtTh3St4rs. So the final serial number was: **"Flag{S0me0fU5#4r3L00king#AtTh3St4rs"**. This was also the flag.

### Appendix A

On first run I got the following:
```
> python runner.py path/to/binary
Traceback (most recent call last):
  File "runner.py", line 4, in <module>
    main()
  File "...ctfs/Codegat2018/hsdecomp/hsdecomp/__init__.py", line 23, in main
    entry_pointer = StaticValue(value = settings.name_to_address[opts.entry])
KeyError: 'Main_main_closure'
```
Well that's not the worst error in the world. After some debugging I was able to figure out the settings.name_to_address dictionary was completely empty. So I looked at metadata.py and found where the dictionary was being initialized. I found the following try exception block with no exception messages being thrown.
```
for sym in symtab.iter_symbols():
    try:
        name = str(sym.name, 'ascii')
        offset = sym['st_value']
        settings.name_to_address[name] = offset
        settings.address_to_name[offset] = name
    except:
        pass

```
After adding an exception message to the except block I found out the issue was the call str(sym.name, 'ascii') was not a valid call so I changed the block to.
```
for sym in symtab.iter_symbols():
    try:
        name = str(sym.name)
        offset = sym['st_value']
        settings.name_to_address[name] = offset
        settings.address_to_name[offset] = name
    except Exception as e:
        print e.message
```
This was a quick fix. I got the following error.
```
python runner.py path/to/binary

Traceback (most recent call last):
  File "runner.py", line 4, in <module>
    main()
  File ".../ctfs/Codegat2018/hsdecomp/hsdecomp/__init__.py", line 71, in main
    print(lhs, "=", show.show_pretty_interpretation(settings, interpretations[pointer]))
  File ".../ctfs/Codegat2018/hsdecomp/hsdecomp/show.py", line 80, in show_pretty_interpretation
    return '\n'.join(render_pretty_interpretation(settings, interp, 0))
  File ".../ctfs/Codegat2018/hsdecomp/hsdecomp/show.py", line 89, in render_pretty_interpretation
    args.append(render_pretty_interpretation(settings, arg, 2))
  File ".../ctfs/Codegat2018/hsdecomp/hsdecomp/show.py", line 89, in render_pretty_interpretation
    args.append(render_pretty_interpretation(settings, arg, 2))
  File ".../ctfs/Codegat2018/hsdecomp/hsdecomp/show.py", line 91, in render_pretty_interpretation
    args.append([show_pretty_nonptr(settings, arg, interp.func)])
  File ".../ctfs/Codegat2018/hsdecomp/hsdecomp/show.py", line 49, in show_pretty_nonptr
    ret += chr(settings.binary[parsed_offset])
TypeError: an integer is required
```
For this error I was getting worried this wasn't going to work but I fixed this error by changing the following code block.

```
***ORIGINAL***
ret = '"'
parsed_offset = settings.rodata_offset + value
while settings.binary[parsed_offset] != 0:
    ret += chr(settings.binary[parsed_offset])
    parsed_offset += 1
ret += '"'
return ret
***END ORIGINAL***

***FIX***
ret = '"'
parsed_offset = settings.rodata_offset + value
while ord(settings.binary[parsed_offset]) != 0:
    try:
        ret += settings.binary[parsed_offset]
        parsed_offset += 1
    except:
        break
ret += '"'
return ret
***END FIX***
```

Basically the settings.binary dictionary contained chars as opposed to integers so I did a quick hack to fix this issue. I was then able to somewhat successfully run the decompiler.
