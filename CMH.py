import socket
import time
import math
import signal
import sys

HOST, PORT = "127.0.0.1", 7777

def send_batch(commands):
    """Send multiple commands in one batch"""
    if not commands:
        return True
        
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1.0)
            s.connect((HOST, PORT))
            
            # Send all commands in one batch
            batch_data = "\n".join(commands) + "\n"
            s.sendall(batch_data.encode())
            return True
            
    except Exception as e:
        print(f"Connection error: {e}")
        return False

def signal_handler(sig, frame):
    print('\nShutting down gracefully...')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# === Camera Animation ===
camera_points = [
    (1040.0, 1130.0, 142.0, 0.0, 0.0, 0.0),   # Start
    (908.0, 1130.0, 128.0, 0.0, 0.0, 0.0),
    (1101.0, 1133.0, 148.0, 0.0, 0.0, 0.0),
    (1063.0, 1088.0, 145.0, 0.0, 0.0, 33.0),
    (683.0, 1036.0, 80.0, 0.0, 0.0, 0.0),
    (1040.0, 1130.0, 142.0, 0.0, 0.0, 0.0)    # Loop to start
]

def lerp(a, b, t):
    return a + (b - a) * t

def lerp_angle(a, b, t):
    """Simple linear interpolation for small angles"""
    # For small rotation values like in your keyframes, simple lerp works better
    return a + (b - a) * t

def interpolate(start, end, t):
    x = lerp(start[0], end[0], t)
    y = lerp(start[1], end[1], t)
    z = lerp(start[2], end[2], t)
    pitch = lerp_angle(start[3], end[3], t)
    yaw = lerp_angle(start[4], end[4], t)
    roll = lerp_angle(start[5], end[5], t)
    return (x, y, z, pitch, yaw, roll)

# === Animation Variables ===
camera_step = 0.005      # 200 FPS
camera_duration = 2.0
steps_per_segment = int(camera_duration / camera_step)

hair_t = 0.0
hair_step_size = 0.02

print("🎥🌈 Starting combined camera + hair color animation...")
print("📊 Batching commands for maximum efficiency")

# Test hair color calculation
test_r = (math.sin(0.0 * 2.0) + 1) / 2
test_g = (math.sin(0.0 * 1.5 + math.pi/2) + 1) / 2
test_b = (math.sin(0.0 * 1.0 + math.pi) + 1) / 2
print(f"🧪 Initial hair test: R={test_r:.3f}, G={test_g:.3f}, B={test_b:.3f}")

while True:
    for i in range(len(camera_points) - 1):
        start = camera_points[i]
        end = camera_points[i + 1]

        for step_idx in range(steps_per_segment):
            # Camera animation
            t = step_idx / steps_per_segment
            cam = interpolate(start, end, t)
            x, y, z, pitch, yaw, roll = cam
            
            cam_cmd = f"CAMSTREAM_{x:.2f}_{y:.2f}_{z:.2f}_{pitch:.2f}_{yaw:.2f}_{roll:.2f}"
            
            # Hair color animation (debug version)
            r = (math.sin(hair_t * 2.0) + 1) / 2
            g = (math.sin(hair_t * 1.5 + math.pi/2) + 1) / 2
            b = (math.sin(hair_t * 1.0 + math.pi) + 1) / 2
            
            # Debug: print hair_t every 50 frames
            if step_idx % 50 == 0:
                print(f"🐛 Debug - hair_t: {hair_t:.3f}, R={r:.3f}, G={g:.3f}, B={b:.3f}")
            
            hair_cmds = [f"HCR.{r:.3f}", f"HCG.{g:.3f}", f"HCB.{b:.3f}"]
            
            # Batch all commands together
            all_commands = [cam_cmd] + hair_cmds
            
            if not send_batch(all_commands):
                print("Connection failed, retrying...")
                time.sleep(0.1)
                continue
                
            print(f"🎥🌈 Cam: {x:.1f},{y:.1f},{z:.1f} R:{roll:.1f} | Hair: R={r:.3f}, G={g:.3f}, B={b:.3f}")
            
            # IMPORTANT: Move hair_t increment here so it actually happens
            hair_t += hair_step_size
            time.sleep(camera_step)