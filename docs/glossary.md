Socket Chat Project — Networking Glossary

Purpose
This dictionary is our reference while building the socket-based chat application.
Rule: Do not memorize these definitions word-for-word. We should be able to explain each concept in our own words and explain what it does in our project.

1. Socket

Simple meaning
A socket is an endpoint that a program uses to communicate over a network.
Think of it like a phone:
- IP address = where the phone is
- Port = which service/person you're calling
- Socket = the communication endpoint your program uses

In Python, sockets are provided by the socket module.
import socket

A TCP socket is commonly created with:
socket.socket(socket.AF_INET, socket.SOCK_STREAM)

What do these mean?
AF_INET — Use IPv4 addresses.
SOCK_STREAM — Use a TCP byte stream.

In our project
Client A ─────┐
Client B ─────┼──► Chat Server
Client C ─────┘
Each client communicates with the server through a socket.

Remember
A socket is the program's network communication endpoint.

2. TCP vs UDP

TCP and UDP are transport-layer protocols.

TCP
TCP = Transmission Control Protocol
TCP provides a reliable, ordered stream of bytes.
Important characteristics:
- Connection-oriented
- Reliable delivery
- Ordered data
- Retransmission when data is lost
- Flow/congestion control
- Byte-stream based
This makes TCP useful for our chat application.

UDP
UDP = User Datagram Protocol
UDP sends independent datagrams without establishing a TCP-style connection.
Important characteristics:
- Connectionless
- No guarantee of delivery
- No guarantee of ordering
- Lower protocol overhead
- Message/datagram oriented
UDP can be useful for things where speed matters more than guaranteed delivery, such as some real-time applications.

For our project
We will use TCP, because a chat application generally should not silently lose messages.

Quick comparison
Feature            TCP           UDP
Connection         Yes           No
Reliable delivery  Yes           No
Ordered data       Yes           No
Retransmission     Yes           No
Data model         Byte stream   Datagrams
Our chat project   YES           NO

Remember
TCP gives us a reliable ordered byte stream; UDP gives us lightweight datagrams without those delivery guarantees.

3. IP Address

An IP address identifies a network interface/device on an IP network.
Example IPv4 address: 192.168.1.20
Another common address is: 127.0.0.1
127.0.0.1 is the IPv4 loopback address. It means: "This computer."
So if our server and client are running on the same computer, we can use: 127.0.0.1

Local network example
Server PC: 192.168.1.10
Client PC: 192.168.1.20
The client could connect to 192.168.1.10 if the network/firewall configuration allows it.

Remember
An IP address identifies where a network endpoint can be reached.

4. Port

An IP address identifies a host/interface, but a computer can run many network services.
A port identifies the service/application endpoint on that host.

Example: 192.168.1.10:5000
Here: 192.168.1.10 = IP address, 5000 = port
Think: IP = building address, Port = apartment/room number

Why do we need ports?
A computer might have:
- Web server → port 80
- HTTPS → port 443
- Our chat server → port 5000
The IP gets the traffic to the machine. The port helps deliver it to the appropriate network service.

Remember
IP tells us which host/interface; port identifies the application endpoint on that host.

5. bind()

bind() associates a socket with a local IP address and port.
Example:
server_socket.bind(("0.0.0.0", 5000))
This tells the operating system that this socket wants to use IP: 0.0.0.0, Port: 5000
0.0.0.0 generally means the server is listening on the available IPv4 interfaces rather than only one specific interface.
For local-only testing, you might instead use:
server_socket.bind(("127.0.0.1", 5000))

Important distinction
bind() does not mean "start accepting clients." It assigns the socket's local network address.

Remember
bind() gives the server socket its local address and port.

6. listen()

listen() changes a TCP socket into a listening socket.
Example:
server_socket.listen()

Conceptually:
Socket created → bind() → listen() → Waiting for clients

The server is now saying: "I am ready to accept incoming TCP connections."

Backlog
You may also see:
server_socket.listen(10)
The number relates to how many pending connections the operating system can queue for acceptance, subject to OS behavior.

Remember
listen() puts a TCP server socket into listening mode.

7. accept()

accept() waits for an incoming TCP connection.
Example:
client_socket, client_address = server_socket.accept()
When a client connects, Python returns: client_socket, client_address
The important idea is that the server keeps its listening socket and receives a new connected socket for communication with that client.

Conceptually:
                  Listening socket
                        │
                        ▼
                   accept()
                   /       \
                  /         \
             Client A     Client B
                │             │
          connected       connected
            socket          socket

Very important
Do not confuse server_socket with client_socket.
The listening socket's job is to accept connections.
The connected client socket's job is to communicate with one particular client.

Remember
accept() waits for a client and returns a new connected socket for that client.

8. connect()

A client uses connect() to request a TCP connection to a server.
Example:
client_socket.connect(("127.0.0.1", 5000))
The client is saying: "Connect my socket to the server at 127.0.0.1 on port 5000."

Conceptually:
CLIENT                         SERVER
connect()
    │
    │  TCP connection request
    ├────────────────────────►
    │
    │                    accept()
    │
    ◄────────────────────────┤
       connection established

Remember
connect() is normally used by the client to establish a TCP connection to a server.

9. send()

send() transmits bytes through a connected socket.
Example:
message = "Hello bro"
client_socket.send(message.encode())
Notice: "Hello bro" is a Python string. Sockets send bytes. So we convert the string: message.encode()

Example:
data = "Hello"
data_bytes = data.encode()
client_socket.send(data_bytes)

Important
send() may send fewer bytes than requested.
For simple learning examples you may see:
sock.send(data)
For robust applications, you should understand sendall(), which keeps sending until all supplied data has been handed off or an error occurs.

Remember
send() sends bytes through the socket.

10. recv()

recv() reads bytes received from a connected socket.
Example:
data = client_socket.recv(1024)
The 1024 is the maximum number of bytes requested for that receive operation. The result is bytes.
To turn it into a string:
message = data.decode()

Example:
data = client_socket.recv(1024)
message = data.decode()
print(message)

Important behavior
recv() can block while waiting for data, depending on the socket's configuration.
Also, recv(1024) does not mean "Give me exactly one message." It means approximately: "Give me up to 1024 bytes that are currently available according to the socket/OS behavior."
This leads to one of the most important concepts in our project: message framing.

11. Why TCP Needs Message Framing

This is one of the MOST IMPORTANT concepts for our project.
TCP is a byte stream.

Suppose the client sends "Hello" and then "World".
The receiver is not guaranteed to receive them as two separate recv() calls.
It might receive:
HelloWorld
Or:
Hel
loWorld
Or:
HelloWo
rld
The network stack does not know that your application considers "Hello" and "World" to be two messages. TCP only knows: BYTES BYTES BYTES BYTES BYTES...

Therefore
Our application needs a message framing rule.
One simple solution is a newline delimiter:
MSG|Josh|Hello bro\n
MSG|Josh|How are you?\n
The receiver collects bytes until it sees \n. Then it knows: "That complete sequence is one application message."

Example
Raw TCP stream:
MSG|Josh|Hello bro\nMSG|Josh|How are you?\n
Application parser:
Message 1: MSG|Josh|Hello bro
Message 2: MSG|Josh|How are you?

Why this matters
Without framing, the receiver cannot reliably know where one application-level message ends and another begins.

Other framing methods
Applications can use:
- Delimiters
- Length prefixes
- Fixed-size messages
- Self-describing formats with a defined framing protocol
For our project, we'll use a simple protocol with explicit message boundaries.

Remember
TCP preserves byte order, not application message boundaries.

12. The Complete Server Flow

The basic TCP server lifecycle is:
socket() → bind() → listen() → accept() → recv()/send() → close()

Think:
Create phone → Choose phone number/address → Turn phone into a waiting service → Answer a caller → Talk → Hang up

13. The Complete Client Flow

A basic TCP client lifecycle is:
socket() → connect() → send()/recv() → close()

Think:
Get phone → Call server → Talk → Hang up

14. Server vs Client Responsibilities

Server
The server generally:
- Creates the listening socket
- Binds an address
- Listens
- Accepts clients
- Receives data
- Processes commands/messages
- Sends responses
- Tracks connected clients
- Handles disconnects

Client
The client generally:
- Creates a socket
- Connects to the server
- Sends commands/messages
- Receives server responses
- Displays information
- Handles disconnects

15. Our Chat Application Mental Model

Eventually our application should look approximately like this:
                 ┌─────────────────────┐
                 │     CHAT SERVER     │
                 │                     │
                 │ listening socket    │
                 │                     │
                 │ client list         │
                 │ protocol parser     │
                 │ message handling    │
                 └──────────┬──────────┘
                            │
             ┌──────────────┼──────────────┐
             │              │              │
             ▼              ▼              ▼
        Client A       Client B       Client C

Each client gets its own connected socket.
The server can then route messages between clients.

16. Python Socket Vocabulary

Term            Meaning
socket()        Creates a socket
AF_INET         IPv4 address family
SOCK_STREAM     TCP-style byte stream
bind()          Assigns local IP/port
listen()        Starts listening for TCP connections
accept()        Accepts a connection
connect()       Client connects to server
send()          Sends bytes
sendall()       Attempts to send all supplied bytes
recv()          Receives bytes
encode()        String → bytes
decode()        Bytes → string
close()         Closes socket
IP address      Identifies a network host/interface
Port            Identifies an application endpoint
TCP             Reliable ordered byte stream
UDP             Connectionless datagram protocol
Framing         Defines where application messages begin/end

17. The Five Things You MUST Understand Before Coding

Before we start building, you should be able to explain these without looking:
1. Socket — "What is a socket?"
2. IP + Port — "Why do we need both an IP address and a port?"
3. Server lifecycle — "What do bind(), listen(), and accept() each do?"
4. Client lifecycle — "What does connect() do?"
5. TCP framing — "If TCP is reliable, why can't we simply assume one send() equals one recv()?"

If you can answer those five questions in your own words, you're ready for the first coding exercise.

18. One-Sentence Memory Cheatsheet

socket()  = create the communication endpoint
bind()    = assign the server's local address/port
listen()  = wait for incoming TCP connections
accept()  = accept one client connection
connect() = client requests a connection
send()    = transmit bytes
recv()    = receive bytes
encode()  = string → bytes
decode()  = bytes → string
framing   = define where application messages end

19. Interview-Level Explanation

Eventually you should be able to say:
"Our chat application uses TCP sockets. The server creates a socket, binds it to an IP address and port, and listens for incoming connections. When a client connects, the server accepts the connection and receives a separate connected socket for that client. Clients use connect() to establish the connection and send/receive bytes through their socket. Because TCP is a byte stream rather than a message protocol, we implement application-level message framing so the receiver can determine where each chat message ends."

That is the level of understanding we're aiming for.

20. Learning Rule

Do not copy code you cannot explain.
For every important piece of code we add to the project, you and your brother should be able to answer:
- What does this line do?
- Why is it necessary?
- What would happen if we removed it?
- What data goes into it?
- What data comes out?
- Where does that data go next?

This dictionary is our reference. The separate project guide will teach the actual construction of the application step-by-step.