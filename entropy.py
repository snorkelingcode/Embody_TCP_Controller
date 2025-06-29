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
step_size = 0.1
delay = 0.05

# 🧬 Morph Targets
morph_keys = [
    "MTHT", "MTHS", "MTHB", "MTHBW", "MTNFT", "MTNF", "MTNS", "MTNBH", "MTNBL",
    "MTEW", "MTEP", "MTEL", "MTFHC", "MTFHCR", "MTFHS", "MTT", "MTEBH", "MTEBW",
    "MTEBA", "MTEC", "MTNB", "MTNL", "MTNW", "MTN", "MTS", "MTCB", "MTCT",
    "MTCD", "MTLO", "MTLW", "MTLOV", "MTLCV", "MTLD", "MTLU", "MTCL", "MTCP",
    "MTCW", "MTJL", "MTJH", "MTH", "MTEYW", "MTEB", "MTND", "MTERS", "MTEYH",
    "MTNCR"
]

# 👗 Outfits
outfits = ["OF.Default", "OF.MaidDress", "OF.PopStar", "OF.Kimono", "OF.BlackDress"]
outfit_pool = outfits.copy()
last_outfit = None

# 🎭 Presets
presets = ["PRS.Fem", "PRS.Fem1"]

# 💇 Hair Styles
hairstyles = ["HS.Default", "HS.Buzz", "HS.Crop"]

# 👁️ Eye saturation memory
current_es = round(random.uniform(10000.0, 20000.0), 3)
es_hold_counter = 0
es_hold_duration = 30  # ~1.5 sec hold at 0.05s per frame

def pick_random_from_pool(pool, last_value=None):
    options = [x for x in pool if x != last_value]
    return random.choice(options) if options else random.choice(pool)

while True:
    # 🎨 Fast hair color
    r = round((math.sin(t * 10.0) + 1) / 2, 3)
    g = round((math.sin(t * 7.5 + math.pi / 2) + 1) / 2, 3)
    b = round((math.sin(t * 5.0 + math.pi) + 1) / 2, 3)
    send(f"HCR.{r}")
    send(f"HCG.{g}")
    send(f"HCB.{b}")

    # 👁️ Eye hue (always random)
    ec = round(random.uniform(0.0, 1.0), 3)

    # 👁️ Eye saturation (70% extreme, 30% normal)
    if es_hold_counter > 0:
        es_hold_counter -= 1
    else:
        if random.random() < 0.7:  # 70% chance for extreme saturation
            current_es = round(random.uniform(10000.0, 20000.0), 3)
            es_hold_counter = es_hold_duration
        else:
            current_es = round(random.uniform(100.0, 1000.0), 3)

    send(f"EC.{ec}")
    send(f"ES.{current_es}")

    # 🟤 Skin color (0.3–2.0)
    skc = round(random.uniform(0.3, 2.0), 3)
    send(f"SKC.{skc}")

    # 🎭 Preset
    preset = random.choice(presets)
    send(preset)

    # 👗 Outfit
    outfit = pick_random_from_pool(outfits, last_outfit)
    send(outfit)
    last_outfit = outfit

    # 💇 Hair style
    hair = random.choice(hairstyles)
    send(hair)

    # 🧬 Morph targets
# 🧬 Morph targets (subtle range)
    morph_values = {}
    for key in morph_keys:
        if key == "MTH":
            val = round(random.uniform(0.0, 0.5), 3)  # Horns
        else:
            val = round(random.uniform(-0.25, 0.5), 3)  # Subtle morphs
        morph_values[key] = val
        send(f"{key}.{val}")

    morph_preview = ", ".join([f"{k}={v}" for k, v in list(morph_values.items())[:3]]) + "..."
    print(f"🎨 Hair: R={r}, G={g}, B={b} | 👁️ EC={ec}, ES={current_es} | 🟤 SKC={skc} | 👗 {outfit} | 🎭 {preset} | 💇 {hair} | 🧬 {morph_preview}")

    t += step_size
    time.sleep(delay)
