# ulitin lang natin ginawa natin sa server
import socket

client = socket.socket(
  socket.AF_INET,
  socket.SOCK_STREAM
)

# cconnect natin yung client sa server
# connect()
client.connect(("127.0.0.1", 8000))
print("connected to the server!")


# nasaloob ng message var yung "_" at magiging byte yung "_"
message = "hi"
client.send(message.encode())

#rrecieved naman natin yung message ng server
dataserver = client.recv(1024)
messageserver = dataserver.decode()
print("server: ", messageserver)