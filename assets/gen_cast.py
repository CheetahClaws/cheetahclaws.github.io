"""Hand-crafted asciinema v2 cast for the cheetahclaws.github.io hero.

Run: python3 gen_cast.py > demo.cast
"""
import json
import sys


HEADER = {
    "version": 2,
    "width": 100,
    "height": 28,
    "timestamp": 1747262400,
    "env": {"SHELL": "/bin/zsh", "TERM": "xterm-256color"},
    "title": "CheetahClaws — review src/api.py with Claude, switch to Ollama, apply fix",
    "idle_time_limit": 1.2,
}

# ANSI helpers
CYAN  = "[36m"
GREEN = "[32m"
YELL  = "[33m"
MAG   = "[35m"
DIM   = "[2m"
BOLD  = "[1m"
GRAY  = "[90m"
RED   = "[31m"
RST   = "[0m"

events = []
t = 0.0

def out(delay, text):
    """Emit a chunk with delay seconds after the previous event."""
    global t
    t += delay
    events.append([round(t, 3), "o", text])

def type_string(s, base=0.04, jitter=0.02):
    """Simulate a human typing — one char at a time, slight jitter."""
    import random
    rng = random.Random(7)
    for ch in s:
        out(base + rng.random() * jitter, ch)

# Scene 1 — shell prompt + cheetahclaws launch
out(0.0, f"{GREEN}~/projects/myapp{RST} {CYAN}❯{RST} ")
out(0.8, "")
type_string("cheetahclaws")
out(0.4, "\r\n")
out(0.3, f"{DIM}[CheetahClaws v3.05.79 · claude-sonnet-4-6 · auto mode]{RST}\r\n")
out(0.2, f"{DIM}Type /help for commands, /model to switch, !cmd for shell, Ctrl+C to quit{RST}\r\n")
out(0.2, "\r\n")
out(0.2, f"{BOLD}{CYAN}[project] »{RST} ")

# Scene 2 — user prompts about security review
out(0.6, "")
type_string("Review src/api.py for security issues and tell me what to fix")
out(0.5, "\r\n\r\n")

# Scene 3 — AI thinks, reads file
out(0.6, f"{DIM}● Reading the file and checking for common patterns…{RST}\r\n")
out(0.4, f"{YELL}[Read]{RST} src/api.py {DIM}(142 lines){RST}\r\n")
out(0.5, f"  {DIM}43:  query = f\"SELECT * FROM users WHERE name = '{{name}}'\"{RST}\r\n")
out(0.2, f"  {DIM}78:  @app.post('/login'){RST}\r\n")
out(0.2, f"  {DIM}96:  return redirect(request.args['next']){RST}\r\n")
out(0.5, f"{YELL}[Grep]{RST} 'execute|cursor' src/ {DIM}(3 matches){RST}\r\n\r\n")

# Scene 4 — AI response, streaming
out(0.6, f"{BOLD}Found 3 issues:{RST}\r\n\r\n")

issues = [
    (f"{RED}1.{RST} {BOLD}SQL injection{RST} {GRAY}— line 43{RST}\r\n",
     f"   f-string interpolation lets a crafted ?name= leak the whole table.\r\n"
     f"   {GREEN}fix:{RST} use a parameterised query — {CYAN}cursor.execute(sql, (name,)){RST}\r\n\r\n"),
    (f"{RED}2.{RST} {BOLD}No rate limiting on /login{RST} {GRAY}— line 78{RST}\r\n",
     f"   no slowapi/flask-limiter; brute-force is trivial.\r\n"
     f"   {GREEN}fix:{RST} add {CYAN}@limiter.limit('5/minute'){RST} or move to fail2ban\r\n\r\n"),
    (f"{RED}3.{RST} {BOLD}Open redirect{RST} {GRAY}— line 96{RST}\r\n",
     f"   ?next= is taken verbatim — phishing payload.\r\n"
     f"   {GREEN}fix:{RST} validate scheme+host against an allowlist before redirect\r\n\r\n"),
]
for title, body in issues:
    out(0.5, title)
    out(0.25, body)

# Scene 5 — switch to local model
out(0.5, f"{BOLD}{CYAN}[project] »{RST} ")
out(0.4, "")
type_string("/model ollama/qwen2.5-coder")
out(0.4, "\r\n")
out(0.4, f"{GREEN}✓{RST} Switched to {BOLD}ollama/qwen2.5-coder{RST} {DIM}(local, no API cost){RST}\r\n\r\n")

# Scene 6 — ask local model to write the fix
out(0.3, f"{BOLD}{CYAN}[project] »{RST} ")
out(0.5, "")
type_string("apply the SQL-injection fix to line 43")
out(0.4, "\r\n\r\n")

out(0.5, f"{YELL}[Edit]{RST} src/api.py {DIM}line 43{RST}\r\n")
out(0.4, f"  {RED}-  query = f\"SELECT * FROM users WHERE name = '{{name}}'\"{RST}\r\n")
out(0.3, f"  {RED}-  rows = cursor.execute(query).fetchall(){RST}\r\n")
out(0.3, f"  {GREEN}+  query = \"SELECT * FROM users WHERE name = ?\"{RST}\r\n")
out(0.3, f"  {GREEN}+  rows = cursor.execute(query, (name,)).fetchall(){RST}\r\n\r\n")
out(0.4, f"{GREEN}✓{RST} Applied. 1 file changed, 2 insertions(+), 2 deletions(-).\r\n\r\n")
out(0.5, f"{BOLD}{CYAN}[project] »{RST} ")
out(0.7, "")  # idle ending

sys.stdout.write(json.dumps(HEADER) + "\n")
for ev in events:
    sys.stdout.write(json.dumps(ev) + "\n")
