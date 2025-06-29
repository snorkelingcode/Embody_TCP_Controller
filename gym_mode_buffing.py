import socket, time, random

HOST, PORT = "127.0.0.1", 7777
bones = ["BNH", "BNC", "BNHD", "BNA", "BNAR", "BNL", "BNF"]

def send(cmd):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall((cmd + "\n").encode())

while True:
    for bone in bones:
        size = round(random.uniform(0.8, 1.2), 2)
        cmd = f"{bone}.{size}"
        print(f"💪 Buffing: {cmd}")
        send(cmd)
        time.sleep(0.3)