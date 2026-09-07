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
