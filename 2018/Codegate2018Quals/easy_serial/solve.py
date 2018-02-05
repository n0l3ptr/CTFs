# coding: utf-8
first = [70, 108, 97, 103, 123, 83, 48, 109, 101, 48, 102, 85, 53]
part1 = ''.join([chr(c) for c in first])
second = [103, 110, 105, 107, 48, 48, 76, 51, 114,52]
part2 = ''.join([chr(c) for c in second])[::-1]
s1b4_info = "abcdefghijklmnopqrstuvwxyz"
loc_7172600 =  9
loc_7172488 =  2
loc_7172584 =  8
loc_7172504 =  3
s1b2_info = "1234567890"
loc_7172568 =  7
loc_7172552 =  6
s1b3_info =  "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
loc_7172536 =  5
loc_7172520 =  4
loc_7172472 =  1
loc_7172456 =  0
loc_7168872 =  48
third = [s1b3_info[loc_7172456],s1b4_info[19], s1b3_info[19], s1b4_info[loc_7172568], s1b2_info[loc_7172488], s1b3_info[18], s1b4_info[19], s1b2_info[loc_7172504], s1b4_info[17], s1b4_info[18]]
part3 = ''.join(third)
print "{}_{}_{}".format(part1,part2,part3)
