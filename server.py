import socket

# we create a socket 1st, btw just imagine the socket as an phone
serversocket = socket.socket( #now may socket na tayo, need natin to store it somewhere
  # chatgpt says that we use address family (IPv4) and socket type (TCP)
  socket.AF_INET, # AF_INET is IPv4, pag gusto natin magswitch sa IPv6 magadd lang tayo ng 6 (AF_INET6)
  socket.SOCK_STREAM # sock_stream para sa TCP
)

# i bind naman daw ngayun yung 'serversocket' sa ip address and port kung saan magwawait yung server ng clients
# gamit tayo bind()
serversocket.bind(("127.0.0.1", 8000))

# ngayon we find / wait for the incoming connection
# listen()
serversocket.listen()
print("server is still waiting for the client...")

# if we find incoming connection we accept it
# accept()
# kukunin din natin yung connected socket and client address

# gawa lang tayo 2 variables for connected socket and client address
client_socket, client_address = serversocket.accept()
print("client connected: ", client_address)



# marereceived ng server ung [data/input] tas nilagay natin sa "data" var sa byte form (1024)
data = client_socket.recv(1024)

# data na sa byte form ddecode sya tas nilagay sa message var
message = data.decode()

print("client: ", message)



#ngayun mag message naman tayo server to client
messageserver = "hello"
client_socket.send(messageserver.encode())























'''
PROBLEM
  ↓
Need network communication
  ↓
Python socket module
  ↓
socket.socket()
  ↓
Need IPv4 + TCP
  ↓
AF_INET + SOCK_STREAM
  ↓
Need local address
  ↓
bind()
  ↓
Need to wait
  ↓
listen()
  ↓
Need to accept clients
  ↓
accept()
'''
