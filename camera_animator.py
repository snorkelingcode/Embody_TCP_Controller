import socket
import time
import math
import signal
import sys

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

# === Camera Keyframes (Original Points) ===
camera_points = [
    (1040.0, 1130.0, 142.0, 0.0, 0.0, 0.0),   # Start
    (908.0, 1130.0, 128.0, 0.0, 0.0, 0.0),
    (1101.0, 1133.0, 148.0, 0.0, 0.0, 0.0),
    (1063.0, 1088.0, 145.0, 0.0, 0.0, 33.0),
    (683.0, 1036.0, 80.0, 0.0, 0.0, 0.0),
    (1040.0, 1130.0, 142.0, 0.0, 0.0, 0.0)    # Loop to start
]

def lerp(a, b, t):
    """Linear interpolation between two values"""
    return a + (b - a) * t

def lerp_angle(a, b, t):
    """Linear interpolation for angles, handling wrap-around"""
    # Normalize angles to [-180, 180] range
    def normalize_angle(angle):
        while angle > 180:
            angle -= 360
        while angle < -180:
            angle += 360
        return angle
    
    a = normalize_angle(a)
    b = normalize_angle(b)
    
    # Find the shortest path between angles
    diff = b - a
    if diff > 180:
        diff -= 360
    elif diff < -180:
        diff += 360
    
    result = a + diff * t
    return normalize_angle(result)

def interpolate(start, end, t):
    """Interpolate between two camera positions with proper rotation handling"""
    x = lerp(start[0], end[0], t)
    y = lerp(start[1], end[1], t)
    z = lerp(start[2], end[2], t)
    pitch = lerp_angle(start[3], end[3], t)
    yaw = lerp_angle(start[4], end[4], t)
    roll = lerp_angle(start[5], end[5], t)
    
    return (x, y, z, pitch, yaw, roll)

def smooth_step(t):
    """Smooth interpolation curve (ease in/out)"""
    return t * t * (3.0 - 2.0 * t)

# === Timing ===
step = 0.005        # 200 FPS
duration = 2.0
steps_per_segment = int(duration / step)

print("🎥 Starting smooth camera animation with rotation support...")
print("📐 Using original camera points with enhanced rotation interpolation")

while True:
    for i in range(len(camera_points) - 1):
        start = camera_points[i]
        end = camera_points[i + 1]

        for step_idx in range(steps_per_segment):
            # Linear interpolation (matching original behavior)
            t = step_idx / steps_per_segment
            
            cam = interpolate(start, end, t)
            x, y, z, pitch, yaw, roll = cam
            
            # Format floats with 2 decimal places and use underscores as delimiters
            cmd = f"CAMSTREAM_{x:.2f}_{y:.2f}_{z:.2f}_{pitch:.2f}_{yaw:.2f}_{roll:.2f}"
            print(f"🎥 {cmd}")
            send(cmd)
            time.sleep(step)