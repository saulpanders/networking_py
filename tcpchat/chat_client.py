# @saulpanders
#8/9/18
# TCP chat client program, to be used with chat_server.py
#NOTE: this is a linux only program

import socket, select, string, sys

def prompt():
	sys.stdout.write('<You> ')
	sys.stdout.flush()

#Main funciton
if __name__ == "__main__":
	
	if (len(sys.argv)<3):
		print "Usage: python chat_client.py hostname port"
		sys.exit()

	host = sys.argv[1]
	port = int(sys.argv[2])

	s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(2)

	#connect ot remote host
	try:
		s.connect((host, port))
	except:
		print "Unable to connect"
		sys.exit()

	print "Connected to remote host, start sending messages"
	prompt()

	while 1:
		socket_list = [sys.stdin, s]

		#get the list sockets that are readable
		read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])

		for sock in read_sockets:
			#incoming messages from remote server
			if sock == s:
				data = sock.recv(4096)
				if not data:
					print "\nDisconnected from chat server"
					sys.exit()
				else:
					#print data
					sys.stdout.write(data)
					prompt()
			else:
				#user entered a message
				msg = sys.stdin.readline()
				s.send(msg)
				prompt()
