import socket, random

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

# Presets
presets = ["PRS.Fem", "PRS.Fem1", "PRS.Masc", "PRS.Masc1"]

# Outfits (no spaces)
outfits = ["OF.Default", "OF.MaidDress", "OF.PopStar", "OF.Kimono", "OF.BlackDress"]

# Hairstyles
hairstyles = ["HS.Default", "HS.Buzz", "HS.Crop"]

# Morph Targets
morph_keys = [
    "MTHT", "MTHS", "MTHB", "MTHBW", "MTNFT", "MTNF", "MTNS", "MTNBH", "MTNBL",
    "MTEW", "MTEP", "MTEL", "MTFHC", "MTFHCR", "MTFHS", "MTT", "MTEBH", "MTEBW",
    "MTEBA", "MTEC", "MTNB", "MTNL", "MTNW", "MTN", "MTS", "MTCB", "MTCT",
    "MTCD", "MTLO", "MTLW", "MTLOV", "MTLCV", "MTLD", "MTLU", "MTCL", "MTCP",
    "MTCW", "MTJL", "MTJH", "MTH", "MTEYW", "MTEB", "MTND", "MTERS", "MTEYH",
    "MTNCR"
]

print("🧬 Press ENTER to randomize character. Ctrl+C to exit.\n")

while True:
    input()  # Wait for Enter key

    # Preset
    preset = random.choice(presets)
    send(preset)

    # Outfit
    outfit = random.choice(outfits)
    send(outfit)

    # Hairstyle
    hair = random.choice(hairstyles)
    send(hair)

    # Skin Color (0.3 – 2.0)
    skc = round(random.uniform(0.2, 5.0), 3)
    send(f"SKC.{skc}")

    # Eye Color (EC) and Saturation (ES)
    ec = round(random.uniform(0.0, 1.0), 3)
    es = round(random.uniform(-10000.0, 20000.0), 3) if random.random() < 0.7 else round(random.uniform(100.0, 1000.0), 3)
    send(f"EC.{ec}")
    send(f"ES.{es}")
    # Morph Targets (subtle + clamped for MTH and MTEP)
    for key in morph_keys:
        if key == "MTH":  # Horns
            val = round(random.uniform(0.0, 0.5), 3)
        elif key == "MTEP":  # Ear Point
            val = round(random.uniform(0.0, 0.5), 3)
        else:
            val = round(random.uniform(-0.7, 0.6), 3)
        send(f"{key}.{val}")


    print(f"✅ Sent: {preset}, {outfit}, {hair}, SKC={skc}, EC={ec}, ES={es} + morphs")
