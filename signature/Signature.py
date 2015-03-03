import hashModule

import math
import sys
import os
import re
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-d", "--data", dest="data", help="Path to a file with data")
parser.add_option("-r", "--report", dest="report", help="Path to a file with report")
parser.add_option("-a", "--action", dest="action", help="A action which will be executed (calc, check)")
(options, args) = parser.parse_args()

if options.action == "check":
	pass
	# if options.report is None:
	# 	print "The file with report must be provided (see help)"
	# 	exit()
elif options.action == "calc":
	if options.report is None:
		options.report = "report.txt"
		print "Creating file for report ({0}/{1})\n".format(os.getcwd(), options.report)
else:
	print "Unrecognized command. (see help)"
	exit()

#
#  Caclulation...
#
##########################################################
def get_signature(path):

	p = int("AF5228967057FE1CB84B92511BE89A47", 16)
	a = int("9E93A4096E5416CED0242228014B67B5", 16)
	q = int("57A9144B382BFF0E5C25C9288DF44D23", 16)

	x = int(os.urandom(16).encode('hex'), 16)
	x = x % (p + 1)
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

	U = int(os.urandom(16).encode('hex'), 16)

	U = int("1458DA6E9B624A5D2999A200E88C3842", 16)

	print "U is {0}".format(format(U, "032x"))

	Z = pow(a, U, p)

	print "Z is {0}".format(format(Z, "032x"))

	Z_sh = (Z * H ) % p
	g = (x * Z * pow(Z_sh, q-2, q) ) % q

	k = (U - g) % q

	S = pow(a, g, p)

	print "g is {0}".format(format(g, "032x"))
	print "k is {0}".format(format(k, "032x"))
	print "S is {0}".format(format(S, "032x"))

	return {"H" : H, "K": k, "S": S, "Y": y}
##########################################################

#
#   Checking...
#
##########################################################
def check():
	print "\nChecking..."
	print "=" * 40
	expo = (H * S * pow(a, k, p)) % p
	left = pow(S, expo, p)
	print "left is  {0}".format(format(left, "032x"))

	expo = (S * pow(a, k, p)) % p
	right = pow(y, expo, p)
	print "right is {0}".format(format(right, "032x"))

	print "=" * 40
##########################################################

#
#	Writing/reading to file...
#
##########################################################
if options.action == "calc":
	sign = get_signature(options.data)
	with open(options.report, "w+") as f:
		f.write("{0}/{1}\n".format(os.getcwd(), options.data))
		f.write("H = {0}\n".format(format(sign["H"], "032x")))
		f.write("Y = {0}\n".format(format(sign["Y"], "032x")))
		f.write("K = {0}\n".format(format(sign["K"], "032x")))
		f.write("S = {0}\n".format(format(sign["S"], "032x")))
else:
	text = None
	path = None
	with open(options.data, "r") as f:
		path = f.readline()
		text = f.read()
	path = path[:len(path) - 1]

	sign = get_signature(path)
	check_sig = re.compile(r"H\s*=\s*(?P<H>[0-9A-Fa-f]+)\s*Y\s*=\s*(?P<Y>[0-9A-Fa-f]+)\s*"
					"K\s*=\s*(?P<K>[0-9A-Fa-f]+)\s*S\s*=\s*(?P<S>[0-9A-Fa-f]+)",
				0).search(text).groupdict()
	print "origin sign => "
	print format(sign["H"], "032x")
	print format(sign["S"], "032x")
	print format(sign["K"], "032x")

	print "read sign ==> "
	print check_sig

	if sign["S"] == int(check_sig["S"], 16) and sign["k"] == int(check_sig["K"], 16):
		print "Sign is correct"
    #print "Result of calculation was saved to {0}/{1}".format(os.getcwd(), options.report)
##########################################################