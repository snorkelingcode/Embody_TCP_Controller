# tcp_emotion_trigger_client.py

import socket
from play_emotion_from_command import play_emotion

HOST = "127.0.0.1"
PORT = 7777

print("🎭 Type an emotion command (EMO.Happy, EMO.Sad, etc), or 'exit' to quit")

while True:
    cmd = input("→ Your Command: ").strip()

    if cmd.lower() == "exit":
        print("👋 Exiting...")
        break

    if cmd.startswith("EMO."):
        emotion = cmd[4:].capitalize()
        play_emotion(emotion)
    else:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.sendall((cmd + "\n").encode('utf-8'))
                print(f"✅ Sent to Unreal: {cmd}")
        except Exception as e:
            print(f"❌ Error: {e}")
