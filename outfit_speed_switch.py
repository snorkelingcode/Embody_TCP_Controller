# outfit_cycle.py
import socket, time

HOST, PORT = "127.0.0.1", 7777
outfits = [
    "OF.Default", "OF.Maid Dress", "OF.Pop Star", "OF.Kimono", "OF.Black Dress"
]

def send(cmd):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall((cmd + "\n").encode())

while True:
    for outfit in outfits:
        print(f"👗 Changing to: {outfit}")
        send(outfit)
        time.sleep(3)
