import http.server
import socketserver
import socket
import threading
import json

# Latest data from plugin
latest_data = {"status": "OFF"}

# ===================== UDP LISTENER ======================
def udp_listener():
    global latest_data

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", 49005))

    print("Listening for TrajPlot data on UDP port 49005...")

    while True:
        packet, addr = sock.recvfrom(2048)
        try:
            data = json.loads(packet.decode())

            # Plugin OFF signal
            if "status" in data and data["status"] == "OFF":
                latest_data = {"status": "OFF"}
                print("Plugin stopped — data reset.")
            else:
                latest_data = data

        except:
            pass


# Start listener thread
threading.Thread(target=udp_listener, daemon=True).start()

# ===================== WEB SERVER ======================
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
