import http.server
import socketserver
import socket
import threading
import json

# Store latest aircraft position
latest_data = {"lat": 0, "lon": 0, "alt": 0, "heading": 0}

# ============ UDP Listener =============
def udp_listener():
    global latest_data

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", 49005))

    print("Listening for LiveMap data on UDP port 49005...")

    while True:
        packet, addr = sock.recvfrom(2048)
        try:
            latest_data = json.loads(packet.decode())
        except:
            pass

# Start UDP listener thread
threading.Thread(target=udp_listener, daemon=True).start()

# ============ Web Server =============
class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/data":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(latest_data).encode())
        else:
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

PORT = 8000
print(f"Web server running at http://localhost:{PORT}")

socketserver.TCPServer.allow_reuse_address = True
server = socketserver.TCPServer(("", PORT), Handler)
server.serve_forever()
