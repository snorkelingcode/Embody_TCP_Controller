# gender_glitch.py
import socket, time

HOST, PORT = "127.0.0.1", 7777
presets = ["PRS.Masc", "PRS.Fem", "PRS.Masc1", "PRS.Fem1"]

def send(cmd):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall((cmd + "\n").encode())

while True:
    for p in presets:
        print(f"🌀 Switching preset: {p}")
        send(p)
        time.sleep(1)
