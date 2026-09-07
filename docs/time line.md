# Build Timeline

A phase-based plan for two people. Adjust dates to your own schedule — the
order matters more than the exact days.

## Phase 0 — Setup (Day 1)

- [x] Both: install Python (or Node), VS Code, Git
- [x] Both: create GitHub repo, add `.gitignore` and `README.md`
- [x] Both: agree on language (Python `socket` vs Node `net`)
- [x] Split roles: **jewelry → server**, **joshua → client**
- [ ] Draw the protocol on paper/Excalidraw: what commands exist
      (`JOIN`, `MSG`, `LEAVE`, `SETINFO`) and what each one carries

## Phase 1 — Bare-bones connection (Day 2–4)

Goal: one server, one client, can send plain text back and forth.

- [x] Member 1: server that listens on a port and accepts one connection
- [x] Member 2: client that connects and sends a hardcoded message
- [x] Both: confirm you can see the message printed on the other side
- [x] Milestone check: can you explain what `bind()`, `listen()`, `accept()`,
      and `connect()` each do? If not, pause and read up before continuing.

## Phase 2 — Multiple clients (Day 5–8)

Goal: server handles more than one client at the same time.

- [ ] Member 1: use threading (one thread per client) or `select()` to
      handle multiple connections
- [ ] Member 1: broadcast — when one client sends a message, all others
      receive it
- [ ] Member 2: client can send and receive messages without blocking
      (needs a listener thread or async loop)
- [ ] Both: test with 3+ client windows open at once

## Phase 3 — Custom protocol (Day 9–12)

Goal: replace raw text with the structured protocol from `README.md`.

- [ ] Both: implement `protocol.py` — shared encode/decode functions used
      by both server and client
- [ ] Member 1: server parses `COMMAND|args` and routes accordingly
- [ ] Member 2: client sends properly formatted commands (`JOIN`, `MSG`,
      `LEAVE`)
- [ ] Both: handle malformed messages without crashing the server

## Phase 4 — CRUD / profile features (Day 13–16)

Goal: users can create and edit basic profile info.

- [ ] Member 2: `SETINFO` command to update username/status
- [ ] Member 1: server stores current user list + their info in memory
      (dictionary), sends updates to clients
- [ ] (Optional) Both: persist users/messages to a local file or SQLite so
      data survives a server restart

## Phase 5 — Polish & edge cases (Day 17–19)

- [ ] Both: handle client disconnects gracefully (no server crash)
- [ ] Both: add basic input validation (empty messages, missing fields)
- [ ] Both: write clear error messages back to the client
- [ ] Both: clean up code, add comments explaining the protocol flow

## Phase 6 — Documentation & demo prep (Day 20–21)

- [ ] Both: finalize `README.md` with setup instructions and screenshots
      or a short terminal recording
- [ ] Both: prepare a 2-minute explanation: what the protocol does, how
      the server handles multiple clients, one bug you hit and fixed
- [ ] Both: push final version to GitHub, tag a release (`v1.0`)

## Stretch Goals (only if time allows)

- [ ] Private messaging between two specific users
- [ ] Simple TUI or web frontend on top of the socket client
- [ ] Dockerize the server for deployment practice
- [ ] Expose the server via a free tunnel (e.g. Cloudflare Tunnel) so it's
      reachable outside your LAN — good next-step networking talking point

## Task Split Summary

| Phase | Member 1 (Server) | Member 2 (Client) |
|---|---|---|
| 0 | Repo setup | Repo setup |
| 1 | Accept connections | Connect + send |
| 2 | Multi-client broadcast | Non-blocking send/receive |
| 3 | Parse protocol | Format protocol |
| 4 | Store user data | Profile edit commands |
| 5 | Disconnect handling | Input validation |
| 6 | Docs + demo | Docs + demo |