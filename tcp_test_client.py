import socket

DEFAULT_HOST = input("Enter target IP (default 127.0.0.1): ").strip() or "127.0.0.1"
DEFAULT_PORT = 7777

print(f"🧠 Connecting to {DEFAULT_HOST}:{DEFAULT_PORT}")
print("Type a word and press Enter to send it to Unreal (type 'exit' to quit)")

while True:
    word = input("→ Your Word: ").strip()

    if word.lower() == "exit":
        print("👋 Exiting...")
        break

    if not word:
        continue  # Skip blank input

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((DEFAULT_HOST, DEFAULT_PORT))
            s.sendall((word + "\n").encode('utf-8'))
            print(f"✅ Sent: {word}")
    except Exception as e:
        print(f"❌ Connection Error: {e}")
