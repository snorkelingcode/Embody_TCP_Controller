# value_sender.py

import socket
import random

HOST, PORT = "127.0.0.1", 7777

def send(cmd):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1.0)
            s.connect((HOST, PORT))
            s.sendall((cmd + "\n").encode())
    except Exception as e:
        print(f"Connection error: {e}")
        return False
    return True

games_played = 0

print("💰 Press ENTER to send finance stats. Ctrl+C to exit.\n")

while True:
    input()  # Wait for Enter key

    # Increment Games Played
    games_played += random.randint(231, 3234)
    send(f"GAMESPLAYED.{games_played}")
    print(f"🎮 Games Played: {games_played}")

    # SARAHGIVE – large in millions
    sarah_give = random.randint(1_000_000, 5_000_000)
    send(f"SARAHGIVE.{sarah_give}")
    print(f"💸 Sarah Give: {sarah_give}")

    # SOLKEEP – realistic 250-500
    sol_keep = random.randint(250, 500)
    send(f"SOLKEEP.{sol_keep}")
    print(f"🔒 SOL Keep: {sol_keep}")

    # SOLGIVE – similar to SOLKEEP
    sol_give = random.randint(250, 500)
    send(f"SOLGIVE.{sol_give}")
    print(f"🤝 SOL Give: {sol_give}")

    print("✅ Finance stats sent.\n")
