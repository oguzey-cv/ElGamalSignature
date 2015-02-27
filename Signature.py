import hashModule

import math
import sys
import os
import re

path = str(sys.argv[1])

def get_number(hex_number):
	number = re.findall('..', hex_number)
	return int("".join(reversed(number)), 16)


# p = get_number("AF5228967057FE1CB84B92511BE89A47")
# a = get_number("9E93A4096E5416CED0242228014B67B5")
# q = get_number("57A9144B382BFF0E5C25C9288DF44D23")

p = int("AF5228967057FE1CB84B92511BE89A47", 16)
a = int("9E93A4096E5416CED0242228014B67B5", 16)
q = int("57A9144B382BFF0E5C25C9288DF44D23", 16)

#x = int(os.urandom(16).encode('hex'), 16)
x = int("74445F42F8DCD66C0343B77ADD7AD38B", 16)
y = pow(a, x, p)

print "p is {0}".format(format(p, "032x"))
print "a is {0}".format(format(a, "032x"))
print "q is {0}".format(format(q, "032x"))
print "x is {0}".format(format(x, "032x"))
print "y is {0}".format(format(y, "032x"))



hash = hashModule.get_hash(path)
str_hash = format(hash, "016x")
print "hash is {0}".format(str_hash)

H = str_hash + "00ffffffffffff00"
H = re.findall('..', H)
H = "".join(reversed(H))
H = int(H, 16)

print "H is {0}".format(format(H, "032x"))

#U = int(os.urandom(16).encode('hex'), 16)

U = int("1458DA6E9B624A5D2999A200E88C3842", 16)

print "U is {0}".format(format(U, "032x"))

Z = pow(a, U, p)

print "Z is {0}".format(format(Z, "032x"))

g = (x * pow(H, p-2, p) % p) % q

k = (U - g) % q

S = pow(a, g, p)

print "g is {0}".format(format(g, "032x"))
print "k is {0}".format(format(k, "032x"))
print "S is {0}".format(format(S, "032x"))


##########################################################

expo = (H * S * pow(a, k, p)) % p
left = pow(S, expo, p)
print "left is {0}".format(format(left, "032x"))

expo = (S * pow(a, k, p)) % p
right = pow(y, expo, p)
print "right is {0}".format(format(right, "032x"))

gh = ((g * H) % p) % q
print "gh % p % q is {0}".format(format(gh, "032x"))
print "g *H % q is {0}".format(format(((g * H) % q), "032x"))
print "g *H % p is {0}".format(format(((g * H) % p), "032x"))
print "x % q is {0}".format(format((x % q), "032x"))
print "x % p is {0}".format(format((x % p), "032x"))
##########################################################