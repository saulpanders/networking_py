# @saulpanders
# simple_portscan.py
# pretty sure the original was from blackhatpython. Added some argparsing & made python3 compliant.

import argparse
from socket import *
from io import *


def main():
	parser = argparse.ArgumentParser(description='Simple port scanner')
	parser.add_argument('-i', '--ip', type=str, help="IP to portscan (default localhost)", default='127.0.0.1')
	parser.add_argument('-s', '--startport', type=int, help="Starting port", default = 1)
	parser.add_argument('-e', '--endport', type=int, help="Ending port", default = 1024)
	args = parser.parse_args()

	ip = args.ip
	start = args.startport
	fin = args.endport

	s = socket (AF_INET,SOCK_STREAM)
	s.settimeout(5)

	print("Scanning ip: ", ip)
	for port in range(start,fin):
		print("Trying port "+ str(port)+"...")
		if (s.connect_ex((ip,port))==0):
			print("PORT ", port, "is OPEN")
	
	s.close()
	print("Scanning Complete")


if __name__ == "__main__":
	main()