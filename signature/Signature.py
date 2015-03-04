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
parser.add_option("-p", "--path", dest="path", help="Path to file during check.")
(options, args) = parser.parse_args()

##########################################################
#
#  Caclulation...
#
##########################################################
def get_common_parameters():
	p = int("AF5228967057FE1CB84B92511BE89A47", 16)
	a = int("9E93A4096E5416CED0242228014B67B5", 16)
	q = int("57A9144B382BFF0E5C25C9288DF44D23", 16)
	return (a, q, p)

def hash_to_number(hash):
	if isinstance(hash, int) or isinstance(hash, long):
		H = format(hash, "016x") + "00ffffffffffff00"
	else:
		H = hash + "00ffffffffffff00"
	H = re.findall('..', H)
	H = "".join(reversed(H))
	return int(H, 16)

def get_signature(path):
	a, q, p = get_common_parameters()
	hash = hashModule.get_hash(path)
	H = hash_to_number(hash)

	x = int(os.urandom(16).encode('hex'), 16)
	x = x % (p + 1)
	y = pow(a, x, p)

	U = int(os.urandom(16).encode('hex'), 16)

	Z = pow(a, U, p)

	Z_sh = (Z * H ) % p
	g = (x * Z * pow(Z_sh, q-2, q) ) % q

	k = (U - g) % q

	S = pow(a, g, p)

	print "\nCaclulation hash ..."
	print "#" * 40
	print "p is {0}".format(format(p, "032x"))
	print "a is {0}".format(format(a, "032x"))
	print "q is {0}".format(format(q, "032x"))
	print "x is {0}".format(format(x, "032x"))
	print "y is {0}".format(format(y, "032x"))
	print "H is {0}".format(format(H, "032x"))
	print "U is {0}".format(format(U, "032x"))
	print "Z is {0}".format(format(Z, "032x"))
	print "g is {0}".format(format(g, "032x"))
	print "k is {0}".format(format(k, "032x"))
	print "S is {0}".format(format(S, "032x"))
	print "#" * 40

	return {"H" : H, 
			"K": k, 
			"S": S, 
			"Y": y,
			"hash": hash}


##########################################################
#
#   Checking...
#
##########################################################
def verification_signature(data):
	a, q, p = get_common_parameters()
	print "\nVerification to correct calculation..."
	print "#" * 40
	common = (data["S"] * pow(a, data["K"], p)) % p

	left = pow(data["S"], (data["H"] * common) % p, p)
	print "left is  {0}".format(format(left, "032x"))

	right = pow(data["Y"], common, p)
	print "right is {0}".format(format(right, "032x"))

	print "#" * 40
	return left == right


##########################################################

#
#	Writing/reading to file...
#
##########################################################
def write_report(sign, path_report, path_orig):
	with open(path_report, "w+") as f:
		f.write("{0}/{1}\n".format(os.getcwd(), path_orig))
		f.write("H = {0}\n".format(format(sign["hash"], "016x")))
		f.write("Y = {0}\n".format(format(sign["Y"], "032x")))
		f.write("K = {0}\n".format(format(sign["K"], "032x")))
		f.write("S = {0}\n".format(format(sign["S"], "032x")))


def read_parse_report(path_report):
	result = {}
	path = None
	text = None
	with open(path_report, "r") as f:
		path = f.readline()
		text = f.read()
	result["path"] = path.strip('\n')
	check_sig = re.compile(r"H\s*=\s*(?P<H>[0-9A-Fa-f]+)\s*Y\s*=\s*(?P<Y>[0-9A-Fa-f]+)\s*"
					"K\s*=\s*(?P<K>[0-9A-Fa-f]+)\s*S\s*=\s*(?P<S>[0-9A-Fa-f]+)",
				0).search(text).groupdict()

	result.update((key, int(value, 16)) for key, value in check_sig.items())
	result["H"] = hash_to_number(result["H"])
	return result

##########################################################
if options.data is None:
	print "File with data must be provided"
	exit()

if options.action == "calc":
	if options.report is None:
		options.report = "report.txt"
		print "Creating file for report ({0}/{1})".format(os.getcwd(), options.report)

	sign = get_signature(options.data)
	verification_signature(sign)
	write_report(sign, options.report, options.data)
	print "\nSignature was successful write to {0}/{1}".format(os.getcwd(), options.report)

elif options.action == "check":
	
	data = read_parse_report(options.data)
	if options.path is None:
		sign = get_signature(data["path"])
	else:
		sign = get_signature(options.path)
	
	if data["H"] == sign["H"] and verification_signature(data) is True:
		print "\nSignature is correct."
	else:
		print "\nSignature is incorrect."
		print "Read data"
		for x, y in data.items():
			if x != "path":
				print "\t{0} is {1}".format(x, format(y, "032x"))
		print "Caclulated signature"
		for x, y in sign.items():
			print "\t{0} is {1}".format(x, format(y, "032x"))
else:
	print "Unrecognized command. (see help)"