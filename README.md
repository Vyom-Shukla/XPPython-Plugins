Collecting workspace information# LiveMap Web - README

## Overview
**LiveMap** is a real-time aircraft tracking system that displays your X-Plane flight position on an interactive web map. It consists of three components:

1. **X-Plane Plugin** (PI_LiveMap.py) - Sends aircraft data via UDP
2. **Python Web Server** (server.py) - Receives UDP data and serves the web interface
3. **Web Interface** (index.html) - Real-time map visualization using Leaflet

---

## Components

### 1. X-Plane Plugin (PI_LiveMap.py)
- Runs inside X-Plane using XPPython3
- Reads aircraft position data (latitude, longitude, altitude, heading)
- Sends data as JSON via UDP to `127.0.0.1:49005` every second
- Includes a menu toggle in X-Plane's Plugins menu to enable/disable tracking

### 2. Web Server (server.py)
- Python HTTP server running on `http://localhost:8000`
- Listens for UDP packets on port `49005`
- Serves static files (index.html)
- Provides `/data` endpoint that returns the latest aircraft position as JSON

### 3. Web Interface (index.html)
- Interactive map using **Leaflet.js** and OpenStreetMap tiles
- Displays aircraft position as a marker
- Shows flight trail as a red polyline
- Updates every 500ms from the server
- Manual zoom/pan control (no auto-centering)

---

## Setup & Usage

### Requirements
- X-Plane with XPPython3 installed
- Python 3.6+
- Modern web browser

### Installation

1. **Copy X-Plane Plugin:**
   - Place PI_LiveMap.py in your X-Plane plugins directory

2. **Start Web Server:**
   ```bash
   python server.py
   ```
   Expected output: `Web server running at http://localhost:8000`

3. **Open Web Interface:**
   - Visit `http://localhost:8000` in your browser

4. **Start Flight:**
   - Launch X-Plane
   - Toggle "LiveMap: ON" in the Plugins menu
   - Your aircraft position will appear on the map

---

## Data Format

Aircraft position is transmitted as JSON:
```json
{
  "lat": 37.7749,
  "lon": -122.4194,
  "alt": 5000,
  "heading": 180
}
```

---

## Notes
- Server only displays the latest received position
- Trail history is maintained only in the browser (resets on refresh)
- UDP updates occur every ~1 second from X-Plane
- Web map updates every 500ms