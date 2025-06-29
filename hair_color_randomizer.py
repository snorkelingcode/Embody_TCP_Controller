import socket, time, math, signal, sys

HOST, PORT = "127.0.0.1", 7777

def send(cmd):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1.0)  # Add timeout
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
step_size = 0.02  # Small increment for smooth changes
delay = 0.05

while True:
    # Three sine waves with different frequencies and phase shifts
    # All values oscillate between 0.0 and 1.0, but at different rates
    r = round((math.sin(t * 2.0) + 1) / 2, 3)                    # Fast oscillation
    g = round((math.sin(t * 1.5 + math.pi/2) + 1) / 2, 3)       # Medium, 90° phase shift
    b = round((math.sin(t * 1.0 + math.pi) + 1) / 2, 3)         # Slow, 180° phase shift
    
    # Send individual RGB commands
    if not (send(f"HCR.{r}") and send(f"HCG.{g}") and send(f"HCB.{b}")):
        print("Connection failed, retrying...")
        time.sleep(1)
        continue
        
    print(f"🌈 Sliding: R={r}, G={g}, B={b}")
    
    t += step_size
    time.sleep(delay)