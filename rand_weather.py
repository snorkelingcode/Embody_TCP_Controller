import socket, time, math, signal, sys

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

def signal_handler(sig, frame):
    print('\nShutting down gracefully...')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

t = 0.0
step_size = 0.1
delay = 0.05

while True:
    # 🌌 Star Brightness: 0.5 – 2.0
    STBR = round(1.25 + 0.75 * math.sin(t * 1.5), 3)
    send(f"STBR.{STBR}")

    # ☁️ Cloud Speed: 0 – 100
    CLDS = round(abs(math.sin(t * 0.3)) * 100, 3)
    send(f"CLDS.{CLDS}")

    # ☁️ Cloud Opacity: 0.2 – 1.0
    CLDO = round(0.6 + 0.4 * math.sin(t * 0.7), 3)
    send(f"CLDO.{CLDO}")

    # 🌞 Sun Height: -1.0 – 1.0
    SNH = round(math.sin(t * 0.5), 3)
    send(f"SNH.{SNH}")

    print(f"🌌 STBR={STBR} | ☁️ CLDS={CLDS}, CLDO={CLDO} | 🌞 SNH={SNH}")

    t += step_size
    time.sleep(delay)
