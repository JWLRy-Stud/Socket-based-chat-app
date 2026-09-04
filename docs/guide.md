Socket-Based Chat App — Build & Learning Guide

Our Mission

y'all are not just trying to "make a chat app." You are going to understand networking by building one.

By the end, both of you should be able to:
- Explain how TCP communication works.
- Build a TCP server from scratch.
- Build a TCP client from scratch.
- Handle multiple clients.
- Design and parse an application protocol.
- Understand TCP message framing.
- Use threads for concurrent clients.
- Store user/chat data.
- Debug network problems.
- Test the application over a LAN.
- Explain the architecture in an interview.
- Read and improve the original GitHub project rather than depending on it.

How We Will Learn

The Golden Rule
Understand → Predict → Code → Break → Debug → Explain → Repeat

We will deliberately avoid building the entire application at once. Every new concept follows this cycle.

1. Understand — Learn what the concept means.
2. Predict — Before running code, predict what will happen.
3. Code — Write a small amount of code.
4. Break — Change something intentionally.
5. Debug — Figure out why it broke.
6. Explain — Explain the concept without reading the notes.
7. Repeat — Use the concept again in a larger part of the application.

This is more useful for long-term retention than simply reading a tutorial.

Important Rule for AI-Assisted Development

We can use ChatGPT as a tutor. But: do not ask for the entire finished project and paste it blindly.

When you need help, prefer:
- "Give us a hint."
- "Explain this error."
- "Why does this line exist?"
- "Give us a smaller example."
- "Review our code."
- "Give us a debugging challenge."

If I give you code, you should be able to explain it afterward.

Project Roadmap

PHASE 0  → Understand the project
PHASE 1  → TCP fundamentals
PHASE 2  → First TCP connection
PHASE 3  → Build a basic server
PHASE 4  → Build a basic client
PHASE 5  → Send messages
PHASE 6  → Multiple clients
PHASE 7  → Threading
PHASE 8  → Protocol design
PHASE 9  → Message framing
PHASE 10 → Chat features
PHASE 11 → User/profile CRUD
PHASE 12 → Persistence/database
PHASE 13 → Robust error handling
PHASE 14 → LAN testing
PHASE 15 → Security improvements
PHASE 16 → Testing
PHASE 17 → Git/GitHub collaboration
PHASE 18 → Resume + interview preparation

Do not skip ahead because a later phase looks more exciting.

PHASE 0 — Understand What We Are Building

Goal
Before writing code, understand the final system. Our application will eventually resemble:

                    ┌──────────────────────┐
                    │      CHAT SERVER     │
                    │                      │
                    │ Listening Socket     │
                    │ Client Manager       │
                    │ Protocol Parser      │
                    │ Message Router       │
                    │ User/Profile Data    │
                    └──────────┬───────────┘
                               │
             ┌─────────────────┼─────────────────┐
             │                 │                 │
             ▼                 ▼                 ▼
         CLIENT A          CLIENT B          CLIENT C

The server is the central coordinator. Clients connect to it.

What We Need to Understand
Before coding, answer:
- What is a socket?
- What is TCP?
- What is an IP address?
- What is a port?
- Why does the server need bind()?
- What does listen() do?
- What does accept() do?
- Why does a client use connect()?
- What does recv() return?
- Why does TCP need application-level message framing?

These answers should come from your own understanding. Use socket_chat_networking_glossary.md as the reference.

----------------------------------------------------------[checkpoint ni manlangit]----------------------------------------------------
aralin ko muna ung nasa taas bago ako magproceed sa baba
----------------------------------------------------------[checkpoint ni manlangit]----------------------------------------------------

Checkpoint 0
Do not continue until y'all can explain the following without reading:

Client → connect() → Server → accept() → Connected socket → send()/recv()

PHASE 1 — TCP FUNDAMENTALS

Goal
Understand what happens before we write a chat application. You should understand:

Application → TCP → IP → Network

Our application uses TCP sockets.

Exercise 1 — Explain TCP
Without looking at the glossary, answer: Why is TCP a reasonable choice for a chat application? Do not worry about making the answer perfect. The goal is retrieval practice.

Exercise 2 — TCP vs UDP
Explain: Why might an application choose UDP instead of TCP?
Then explain: Why are we choosing TCP?

Exercise 3 — IP + Port
Suppose the server is: 192.168.1.10:5000
Explain what 192.168.1.10 and 5000 each identify.

Checkpoint 1
You pass this phase when you can explain TCP, UDP, IP, port, and socket in your own words.

PHASE 2 — YOUR FIRST TCP CONNECTION

Goal
Create the smallest possible TCP server and client. Do NOT build chat yet. We want:

Client ─────────► Server
          Hello

That's it.

Step 1 — Create a server socket
Start by learning:

import socket

server_socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

Do not memorize it. Understand AF_INET and SOCK_STREAM.

Prediction
Before running it: what do you think this code does? Write your answer down. Then run it.

Step 2 — Bind
Next, learn:

server_socket.bind(("127.0.0.1", 5000))

Question: Why does the server need a port?
Question: What do you think happens if another program is already using port 5000? Test it.

Step 3 — Listen
Learn:

server_socket.listen()

Question: What changed after calling listen()?

Step 4 — Accept
Learn:

client_socket, client_address = server_socket.accept()

Important: accept() waits. That means your program may appear to "freeze." It isn't necessarily frozen — it may simply be waiting for a client.

Experiment
Run the server. Observe what happens before a client connects. Then create the client. Observe what changes.

PHASE 3 — BUILD THE FIRST CLIENT

Goal
Connect to our server. The client begins with:

import socket

client_socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

Then:

client_socket.connect(("127.0.0.1", 5000))

Mental Model

SERVER                          CLIENT

socket()
bind()
listen()

                                socket()
                                connect()
                  ◄───────────────
accept()

Experiment
Run Server and Client in separate terminals. Observe the order.

Debugging Challenge
Change 5000 on the client to 5001. What happens? Do not immediately ask for the answer. Predict first. Then run it. Then explain the error. This is deliberate debugging practice.

PHASE 4 — SEND AND RECEIVE DATA

Goal
Make the client send something.
Client: Hello server!
Server: Hello client!

Important Concept: Bytes
Sockets communicate using bytes. Therefore message = "Hello" needs to become bytes, for example message.encode(). The server receives bytes and can decode them: data.decode()

Exercise
Predict the difference between "Hello" and b"Hello". Then test it.

PHASE 5 — BUILD A TINY CHAT

Goal
Turn the one-message experiment into:

Client
  │
  │ message
  ▼
Server
  │
  │ response
  ▼
Client

Do not add multiple clients yet. Do not add threading yet. Do not add databases yet. Master one connection first.

Challenge
Make the client send: Hello bro
The server should respond: Message received!
Then reverse the direction.

PHASE 6 — UNDERSTAND THE BIG PROBLEM

Goal
Understand why a basic chat program is not enough.

Imagine the client does:
send("Hello")
send("World")

Can the server assume recv() → "Hello" and recv() → "World"? NO.

TCP provides a byte stream. It does not preserve your application's message boundaries.

Experiment
Try sending multiple pieces of data. Observe what the receiver gets. The exact behavior can vary. That is the lesson.

PHASE 7 — MESSAGE FRAMING

Goal
Teach the application how to identify message boundaries.

We can use a delimiter, for example:
Hello\n
World\n

The application can interpret \n as: End of message.

Mental Model
TCP sees: H e l l o \n W o r l d \n
Our application interprets: Message 1 = Hello, Message 2 = World

Exercise
Design three possible framing systems: newline delimiter, length prefix, fixed-size messages. Write one advantage and disadvantage of each. Then we'll choose one for the project.

PHASE 8 — MULTIPLE CLIENTS

Goal
Connect Client A, Client B, and Client C to one server. The server needs to keep track of clients.

Conceptually:
clients = []

But do not stop at copying that. Ask: Why does the server need to remember connected clients?
Answer: Because eventually it needs to send messages to other clients.

PHASE 9 — THREADING

Goal
Understand concurrency.

A naive server might do:
accept Client A → talk to Client A → finish Client A → accept Client B

That creates a problem. If Client A stops responding, the server waits, Client B waits, Client C waits.

We want:

                 Server
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
     Thread A   Thread B   Thread C
        │          │          │
     Client A   Client B   Client C

Important Learning Point
A thread is not "another computer." It is a separate execution path inside the process. For this project, a thread can handle one connected client.

Exercise
Explain: Why would a server want a separate thread for each client?
Then explain: What problems can happen when multiple threads access the same client list?

This prepares you for synchronization and race conditions.

PHASE 10 — DESIGN OUR PROTOCOL

Goal
Stop sending random strings. We need a language between client and server, for example:

JOIN|Josh
MSG|Josh|Hello bro
LEAVE|Josh

This is our application-layer protocol.

Why?
The server needs to distinguish "Hello" from "login" from "send a message" from "change profile."

Protocol Design Exercise
Before coding, design commands for: LOGIN, LOGOUT, MESSAGE, PROFILE, LIST USERS.
For each command decide: command name, required fields, optional fields, server response, error response. Do this on paper first.

PHASE 11 — PROTOCOL PARSING

Goal
Turn raw data into structured commands.

Example:
MSG|Josh|Hello
becomes conceptually:
command = MSG, user = Josh, message = Hello

Important Rule
Never assume the client always sends valid data. Eventually we need to handle:
MSG
MSG|
MSG||Hello
UNKNOWN|data

This introduces validation, error handling, and defensive programming.

PHASE 12 — CHAT FEATURES

Now we can start implementing real chat behavior.

Basic
- Username
- Join
- Leave
- Broadcast messages
- Online user list

Intermediate
- Private messages
- Change username
- Profile information
- Message history

Advanced
- Authentication
- Password hashing
- Persistent chat history
- Rooms
- Reconnection
- Rate limiting

Do not implement all advanced features immediately. Build one feature at a time.

PHASE 13 — USER / PROFILE CRUD

CRUD means:
C = Create
R = Read
U = Update
D = Delete

Teaching Strategy
Before coding CRUD, explain what CRUD means using something unrelated to programming.

Example — Student record:
CREATE → add student
READ   → view student
UPDATE → change student
DELETE → remove student

Then apply the same concept to the chat application.

PHASE 14 — PERSISTENCE

Problem
If we stop the server, what happens to our data?

If everything exists only in memory:
SERVER START → data exists
SERVER STOP → data disappears

We need persistence.

Possible Storage
Start simple: JSON/file
Then consider: SQLite

For a resume project, understanding why we selected a storage method matters more than blindly adding a database.

PHASE 15 — ERROR HANDLING

A real network application must expect things to go wrong. Examples:
- Client disconnects unexpectedly
- Server shuts down
- Invalid command
- Malformed message
- Port already occupied
- Connection refused
- Broken connection
- Timeout

Exercise
For every error: What happened? What caused it? What should the server do? What should the client do? What should the user see?

This turns debugging into engineering.

PHASE 16 — LAN TESTING

Goal
Stop testing only 127.0.0.1 and test:

Computer A
     │
     │ LAN
     ▼
Computer B

Find the server's LAN IP, for example 192.168.1.10, then:
Client → 192.168.1.10:5000 → Server

Problems We Expect
You may encounter: firewall blocking the port, wrong IP, wrong port, server bound only to loopback, different networks, router isolation, connection refused. These are not failures of the project — they are networking lessons.

PHASE 17 — TESTING

We don't just test "It works." We test specific behaviors.

TEST 1  — One client connects
TEST 2  — Two clients connect
TEST 3  — Client A sends message
TEST 4  — Client A disconnects
TEST 5  — Client B sends message after A leaves
TEST 6  — Invalid command
TEST 7  — Very long message
TEST 8  — Multiple messages quickly
TEST 9  — Server shutdown
TEST 10 — Client reconnects

PHASE 18 — GIT AND TEAMWORK

y'all should practice real collaboration.

Suggested structure:
main
│
├── feature/server
├── feature/client
├── feature/protocol
├── feature/database
└── feature/testing

Do not both constantly edit the exact same file. Divide responsibilities.

Suggested Team Split

You — Focus initially on: Server, Networking, TCP, Threading, Client management

Brother — Focus initially on: Client, Protocol interaction, User interface, CRUD, Testing

Then switch/review each other's work. The goal is for both people to understand everything.

PHASE 19 — CODE REVIEW

When either of you finishes a feature, ask:
- Understanding — Can I explain every important line?
- Design — Why did we structure it this way?
- Reliability — What happens if something goes wrong?
- Networking — What happens on the wire?
- Maintainability — Can another developer understand this?
- Testing — How did we prove it works?

PHASE 20 — RESUME QUALITY

A project becomes more impressive when you can demonstrate engineering decisions. Document:
Architecture, Protocol, Networking, Concurrency, Data storage, Testing, Error handling, Security, Known limitations, Future improvements.

Create an architecture diagram. Example:

┌──────────────┐
│   Client A   │
└──────┬───────┘
       │ TCP
       ▼
┌────────────────────┐
│                    │
│    Chat Server     │
│                    │
│  Connection Layer  │
│        ↓           │
│  Protocol Parser   │
│        ↓           │
│  Chat Logic        │
│        ↓           │
│  Data Layer        │
│                    │
└─────────┬──────────┘
          │
          ▼
     ┌─────────┐
     │ Storage │
     └─────────┘

HOW I WILL TEACH YOU DURING THE PROJECT

Whenever you come back and say "We're on Phase 4," I will teach from this guide rather than jumping randomly ahead.

If you show me code, I will prioritize:
1. Ask what you think is happening.
2. Identify the misconception.
3. Give a hint.
4. Let you attempt it.
5. Review your attempt.
6. Explain the underlying concept.
7. Give a small challenge.

If you are completely stuck, we can progressively increase the help:
LEVEL 1 — Question
LEVEL 2 — Hint
LEVEL 3 — Small example
LEVEL 4 — Partial solution
LEVEL 5 — Full explanation

Try to stay at the lowest level of help that gets you unstuck.

THE "TEACH IT BACK" RULE

After learning an important concept, one of you should explain it to the other.

Example:
Brother A: "What does accept() do?"
Brother B: "The server uses it to wait for and accept an incoming TCP connection. It returns a new connected socket that communicates with that particular client."

Then switch roles. If the explanation is wrong, that's useful — it shows us exactly what needs to be reviewed.

WEEKLY RETENTION SYSTEM

Do not learn something once and assume you remember it. Use spaced retrieval.

Day 0  — Learn concept.
Day 1  — Explain concept without notes.
Day 3  — Solve a small problem.
Day 7  — Explain it again.
Day 14 — Use it in the project.
Day 30 — Explain the architecture from memory.

This is especially important for networking terminology.

FINAL INTERVIEW TEST

When the project is complete, you should be able to answer:

Networking
- What is a socket?
- Why TCP instead of UDP?
- What is an IP address?
- What is a port?
- What does bind() do?
- What does listen() do?
- What does accept() do?
- What does connect() do?
- What does send() do?
- What does recv() do?

TCP
- Is TCP message-oriented?
- Why does message framing matter?
- What happens when a client disconnects?
- Why might one recv() not equal one send()?

Server
- How does your server handle multiple clients?
- Why did you use threads?
- What happens if one client crashes?
- How do you track connected clients?

Protocol
- Why did you create an application protocol?
- How are commands represented?
- How does the server validate commands?
- How are errors returned?

Architecture
- Explain the entire system from client to server and back.
- Where is networking handled?
- Where is application logic handled?
- Where is data stored?

Engineering
- How did you test the application?
- What happens when the server goes down?
- What security problems remain?
- What would you improve if you had another month?

If you can answer these naturally, you don't merely have a GitHub project. You understand the project.

FIRST TASK

Do NOT start writing the complete chat application. Your first assignment is:

Task A
Read: socket_chat_networking_glossary.md

Task B
Close the glossary. Without looking, explain to your brother: socket, TCP, IP, port, bind(), listen(), accept(), connect(), send(), recv(), message framing.

Task C
Draw this from memory:

Client
   │
   │ connect()
   ▼
Server
   │
   │ accept()
   ▼
Connected socket
   │
   ├── send()
   └── recv()

Task D
Answer this question: If TCP is reliable, why can't we assume that every send() from the client corresponds to exactly one recv() on the server? Write your answer in your own words.
