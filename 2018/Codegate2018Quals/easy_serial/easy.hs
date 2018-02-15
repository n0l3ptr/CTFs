Main_main_closure = >> $fMonadIO
    (putStrLn (unpackCString# "Input Serial Key >>> "))
    (>>= $fMonadIO
        getLine
        (\s1dZ_info_arg_0 ->
            >> $fMonadIO
                (putStrLn (++ (unpackCString# "your serial key >>> ") (++ s1b7_info (++ (unpackCString# "_") (++ s1b9_info (++ (unpackCString# "_") s1bb_info)))))) #Print out three chunks with _
###FIRST CHUNK
                (case && (== $fEqInt (ord (!! s1b7_info loc_7172456)) (I# 70)) 
		(&& (== $fEqInt (ord (!! s1b7_info loc_7172472)) (I# 108)) 
		(&& (== $fEqInt (ord (!! s1b7_info loc_7172488)) (I# 97)) 
		(&& (== $fEqInt (ord (!! s1b7_info loc_7172504)) (I# 103)) 
		(&& (== $fEqInt (ord (!! s1b7_info loc_7172520)) (I# 123)) 
		(&& (== $fEqInt (ord (!! s1b7_info loc_7172536)) (I# 83)) 
		(&& (== $fEqInt (ord (!! s1b7_info loc_7172552)) (I# 48)) 
		(&& (== $fEqInt (ord (!! s1b7_info loc_7172568)) (I# 109)) 
		(&& (== $fEqInt (ord (!! s1b7_info loc_7172584)) (I# 101)) 
		(&& (== $fEqInt (ord (!! s1b7_info loc_7172600)) (I# 48)) 
		(&& (== $fEqInt (ord (!! s1b7_info (I# 10))) (I# 102)) 
		(&& (== $fEqInt (ord (!! s1b7_info (I# 11))) (I# 85)) 
		(== $fEqInt (ord (!! s1b7_info (I# 12))) (I# 53))))))))))))) of
                    <tag 1> -> putStrLn (unpackCString# ":p"),
###SECOND CHUNK                    
		c1ni_info_case_tag_DEFAULT_arg_0@_DEFAULT -> case == ($fEq[] $fEqChar) (reverse s1b9_info) 
		(: (C# 103) (: (C# 110) (: (C# 105) (: (C# 107) (: loc_7168872 (: loc_7168872 (: (C# 76) (: (C# 51) (: (C# 114) (: (C# 52) [])))))))))) of
                        False -> putStrLn (unpackCString# ":p"),
##THIRD CHUNK
                        True -> case && 
		(== $fEqChar (!! s1bb_info loc_7172456) (!! s1b3_info loc_7172456)) 
		(&& (== $fEqChar (!! s1bb_info loc_7172472) (!! s1b4_info (I# 19))) 
		(&& (== $fEqChar (!! s1bb_info loc_7172488) (!! s1b3_info (I# 19))) 
		(&& (== $fEqChar (!! s1bb_info loc_7172504) (!! s1b4_info loc_7172568)) 
		(&& (== $fEqChar (!! s1bb_info loc_7172520) (!! s1b2_info loc_7172488)) 
		(&& (== $fEqChar (!! s1bb_info loc_7172536) (!! s1b3_info (I# 18))) 
		(&& (== $fEqChar (!! s1bb_info loc_7172552) (!! s1b4_info (I# 19))) 
		(&& (== $fEqChar (!! s1bb_info loc_7172568) (!! s1b2_info loc_7172504)) 
		(&& (== $fEqChar (!! s1bb_info loc_7172584) (!! s1b4_info (I# 17))) 
		(== $fEqChar (!! s1bb_info loc_7172600) (!! s1b4_info (I# 18))))))))))) of
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
