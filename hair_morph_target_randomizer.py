import socket, time, math, signal, sys, random

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
step_size = 0.1  # Larger step size = faster animation
delay = 0.05     # Faster frame rate

# 🎭 All morph target keys
morph_keys = [
    "MTHT", "MTHS", "MTHB", "MTHBW", "MTNFT", "MTNF", "MTNS", "MTNBH", "MTNBL",
    "MTEW", "MTEP", "MTEL", "MTFHC", "MTFHCR", "MTFHS", "MTT", "MTEBH", "MTEBW",
    "MTEBA", "MTEC", "MTNB", "MTNL", "MTNW", "MTN", "MTS", "MTCB", "MTCT",
    "MTCD", "MTLO", "MTLW", "MTLOV", "MTLCV", "MTLD", "MTLU", "MTCL", "MTCP",
    "MTCW", "MTJL", "MTJH", "MTH", "MTEYW", "MTEB", "MTND", "MTERS", "MTEYH",
    "MTNCR"
]

while True:
    # ⚡ Faster RGB oscillation
    r = round((math.sin(t * 10.0) + 1) / 2, 3)
    g = round((math.sin(t * 7.5 + math.pi/2) + 1) / 2, 3)
    b = round((math.sin(t * 5.0 + math.pi) + 1) / 2, 3)

    if not (send(f"HCR.{r}") and send(f"HCG.{g}") and send(f"HCB.{b}")):
        print("⚠️ Hair color send failed. Retrying...")
        time.sleep(1)
        continue

    # 🧬 Morph targets: aggressive randomization
    morph_values = {}
    for key in morph_keys:
        val = round(random.uniform(-1.0, 2.0), 3)
        morph_values[key] = val
        if not send(f"{key}.{val}"):
            print(f"⚠️ Failed to send morph: {key}")

    morph_preview = ", ".join([f"{k}={v}" for k, v in list(morph_values.items())[:5]]) + "..."
    print(f"🎨 Hair: R={r}, G={g}, B={b} | 🧬 Morphs: {morph_preview}")

    t += step_size
    time.sleep(delay)
