# Socket-Based Chat App

A multi-user chat application built on **raw TCP sockets** — no web framework
handling the networking. Client-server connections, message framing, and a
custom text protocol are all implemented by hand, alongside basic CRUD
features (post messages, edit profile info).

This project exists to demonstrate real networking fundamentals (sockets,
connections, protocol design) for a Network Engineer OJT/job application —
not just app-building skills.

## Features

- [ ] Multiple clients can connect to a central server at once
- [ ] Real-time message broadcast to all connected clients
- [ ] Basic user profile (username, status message) — create / edit / view
- [ ] Custom lightweight protocol over TCP (see below)
- [ ] Graceful handling of client disconnects
- [ ] (Stretch) Private messaging between two users
- [ ] (Stretch) Persist chat history to a local file or SQLite

## Tech Stack

- **Language:** Python (`socket`, `threading`) — swap to Node.js (`net`
  module) if the team prefers
- **No external frameworks** for the core networking layer — this is the
  point of the project
- **Storage:** plain file or SQLite for chat history / user profiles
  (optional, no paid services)

## Custom Protocol

Messages are sent as plain text lines terminated by `\n`. Format:

```
COMMAND|arg1|arg2|...\n
```

Examples:

```
MSG|josh|hello everyone\n
JOIN|josh\n
LEAVE|josh\n
SETINFO|josh|status=studying networking\n
```

The server parses each line by splitting on `|`, then routes it based on the
`COMMAND` value. This is intentionally simple — the goal is to be able to
explain, line by line, how a message travels from one client to another.

## Project Structure

```
chat-app/
├── server/
│   └── server.py        # accepts connections, broadcasts messages
├── client/
│   └── client.py        # connects to server, sends/receives messages
├── protocol.py           # shared message encode/decode helpers
├── README.md
├── TIMELINE.md
└── .gitignore
```

## Getting Started

```bash
# 1. Clone the repo
git clone <your-repo-url>
cd chat-app

# 2. Run the server (default port 5000)
python server/server.py

# 3. In separate terminals, run one or more clients
python client/client.py
```

No API keys, no paid services, no external dependencies required to run the
core version.

## Team

- **Member 1:** John Joshua Manlangit — server logic, protocol design
- **Member 2:** [partner's name] — client logic, profile/CRUD features

See `TIMELINE.md` for the build plan and task split.

## Why This Project

Most beginner portfolio projects hide networking behind a web framework.
This one doesn't — every connection, every message, and every disconnect is
handled explicitly, which makes it a strong talking point for networking-
focused interviews and OJT applications.