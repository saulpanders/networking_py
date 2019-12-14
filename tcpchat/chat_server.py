#Paul Sanders
#8/9/18
#TCP chat server program, to be used with chat_client.py
#NOTE: this is a linux only program
import socket, select

#Function to broadcast messages to all clients
def broadcast_data(sock, message):
	#Don't send message to master socket & client who has sent us the message
	for socket in CONNECTION_LIST:
		if socket!=server_socket and socket != sock:
			try:
				socket.send(message)
			except:
				#broken socket connection
				socket.close()
				CONNECTION_LIST.remove(socket)

if __name__=="__main__":
	
	#List to keep track of socket descriptors
	CONNECTION_LIST = []
	RECV_BUFFER = 4096
	PORT = 5000

	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.bind(("0.0.0.0", PORT))
	server_socket.listen(10)

	#Add server socket to list of readable connections
	CONNECTION_LIST.append(server_socket)

	print "Chat server started on port " + str(PORT)

	while 1:
		#Get list of sockets ready to be read through select()
		read_sockets, write_sockets, error_sockets = select.select(CONNECTION_LIST,[], [])

		for sock in read_sockets:
			#New connection
			if sock == server_socket:
				#Handle the case in which there is a new connection received
				sockfd, addr = server_socket.accept()
				CONNECTION_LIST.append(sockfd)
				print "Client (%s, %s) connected" % addr

				broadcast_data(sockfd, "[%s:%s] entered room\n" % addr)
			#some incoming message from client
			else:
				#process data from client
				try:
					data = sock.recv(RECV_BUFFER)
					if data:
						broadcast_data(sock, "\r"+'<' + str(sock.getpeername())+'>'+ data)
				except:
					broadcast_data(sock, "Client (%s,%s) is offline" % addr)
					print "Client (%s,%s) is offline" % addr
					sock.close()
					CONNECTION_LIST.remove(sock)
					continue
	server_socket.close()