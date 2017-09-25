lower = "}0y_3d0m"

sums = [0x2df, 0x290, 0x209, 0x27b, 0x1f9, 0x25e, 0x229, 0x211]

matrix = []
results = []

#set up first equation
eq1 = [0 for _ in range(8)]
eq1[0] = 1
matrix.append(eq1)
results.append(ord('}'))

#first
eq2 = [0, 1, 1, 1, 1, 1, 1, 1]
matrix.append(eq2)
results.append(0x211+0x29+0x2)

#second
#(may need to change this)
eq2 = [1, 0, 1, 1, 1, 1, 1, 1]
matrix.append(eq2)
results.append(0x229+0x5e+0x2)

#third
eq2 = [1, 1, 0, 1, 1, 1, 1, -1]
matrix.append(eq2)
results.append(0x25e-0xf9+0x1)

#fourth
eq2 = [1, 1, 1, 0, 1, 1, 1, -1]
matrix.append(eq2)
results.append(0x1f9-0x7b+0x2)

#fifth
eq2 = [1, 1, 1, 1, 0, 1, 1, 1]
matrix.append(eq2)
results.append(0x27b+0x9+0x2)

#sixth
eq2 = [1, 1, 1, 1, 1, 0, 1, -1]
matrix.append(eq2)
results.append(0x209-0x90+0x2)

#seventh
eq2 = [1, 1, 1, 1, 1, 1, 0, -1]
matrix.append(eq2)
results.append(0x290-0xdf-0x2)

print "Plug this into sage:"
print

print "A = matrix(", matrix, ')'
print "v = vector(", results, ')'
print "A.solve_right(v)\n"
print "''.join(chr(x) for x in _)"

#now plug into sage
sums = [0x270, 0x255, 0x291, 0x233, 0x278, 0x221, 0x25d, 0x28f]

matrix = []
results = []

#set up first equation
eq1 = [0 for _ in range(8)]
eq1[3] = 1
matrix.append(eq1)
results.append(ord('{'))

#first
eq2 = [0, 1, 1, 1, 1, 1, 1, 1]
matrix.append(eq2)
results.append(0x270+0x55+0x2)

#second
#(may need to change this)
eq2 = [1, 0, 1, 1, 1, 1, 1, -1]
matrix.append(eq2)
results.append(0x255-0x91+0x2)

#third
eq2 = [1, 1, 0, 1, 1, 1, 1, 1]
matrix.append(eq2)
results.append(0x291+0x33+0x2)

#fourth
eq2 = [1, 1, 1, 0, 1, 1, 1, -1]
matrix.append(eq2)
results.append(0x233-0x78+0x2)

#fifth
eq2 = [1, 1, 1, 1, 0, 1, 1, 1]
matrix.append(eq2)
results.append(0x278+0x21+0x2)

#sixth
eq2 = [1, 1, 1, 1, 1, 0, 1, 1]
matrix.append(eq2)
results.append(0x221+0x5d+0x2)

#seventh
eq2 = [1, 1, 1, 1, 1, 1, 0, -1]
matrix.append(eq2)
results.append(0x25d-0x8f-0x2)

print "A = matrix(", matrix, ')'
print "v = vector(", results, ')'
print "A.solve_right(v)\n"
print "''.join(chr(x) for x in _)"

#now plug into sage and get:
upper = '3r4{_zla'
lower = "}0y_3d0m"

#unjumble (blocks of 4)
jumbled = "3r4{_zla}0y_3d0m"
flag = "}0y_3d0m_zla3r4{"
print flag[::-1]
