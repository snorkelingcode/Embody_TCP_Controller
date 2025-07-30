#!/usr/bin/env python3
"""
HTTP to TCP Bridge Server
Receives HTTP POST requests from the web UI and forwards them as TCP to port 7777.

Usage: python http_tcp_bridge.py
This will create an HTTP server on port 8080 that forwards commands to TCP port 7777.
"""

import socket
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Configuration
TCP_HOST = '127.0.0.1'
TCP_PORT = 7777
HTTP_HOST = '127.0.0.1'  
HTTP_PORT = 8080

class TCPBridgeHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        """Handle POST requests with TCP commands"""
        try:
            # Read the command from POST data
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            # Parse command
            data = json.loads(post_data)
            command = data.get('command', '').strip()
            
            if not command:
                self.send_error_response("No command provided")
                return
            
            # Send to TCP server (same way as tcp_test_client.py)
            success = self.send_tcp_command(command)
            
            if success:
                self.send_success_response(f"Command sent: {command}")
                print(f"✅ Sent to TCP: {command}")
            else:
                self.send_error_response("Failed to send to TCP server")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            self.send_error_response(str(e))
    
    def send_tcp_command(self, command):
        """Send command to TCP server using same method as tcp_test_client.py"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((TCP_HOST, TCP_PORT))
                s.sendall((command + "\n").encode('utf-8'))
                return True
        except Exception as e:
            print(f"❌ TCP Error: {e}")
            return False
    
    def send_success_response(self, message):
        """Send successful JSON response"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = json.dumps({"success": True, "message": message})
        self.wfile.write(response.encode('utf-8'))
    
    def send_error_response(self, error):
        """Send error JSON response"""
        self.send_response(400)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = json.dumps({"success": False, "error": error})
        self.wfile.write(response.encode('utf-8'))
    
    def log_message(self, format, *args):
        """Suppress default HTTP logging"""
        pass

def main():
    print("🚀 Starting HTTP-to-TCP Bridge")
    print(f"📡 HTTP Server: http://{HTTP_HOST}:{HTTP_PORT}")
    print(f"🎯 TCP Target: {TCP_HOST}:{TCP_PORT}")
    
    # Test TCP connection
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as test_socket:
            test_socket.settimeout(2)
            test_socket.connect((TCP_HOST, TCP_PORT))
            print(f"✅ TCP server is reachable at {TCP_HOST}:{TCP_PORT}")
    except Exception as e:
        print(f"⚠️  Warning: Cannot reach TCP server - {e}")
        print(f"🔧 Make sure your game/TCP server is running on port {TCP_PORT}")
    
    # Start HTTP server
    server = HTTPServer((HTTP_HOST, HTTP_PORT), TCPBridgeHandler)
    print(f"🟢 Bridge server running!")
    print(f"🛑 Press Ctrl+C to stop")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Bridge server stopped")
        server.shutdown()

if __name__ == "__main__":
    main()