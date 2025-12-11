# LiveMapWeb - X-Plane Plugin Ecosystem

## Overview
**LiveMapWeb** is a comprehensive X-Plane plugin ecosystem for real-time data visualization. It provides multiple tools for monitoring and analyzing flight data, including live aircraft tracking on interactive maps and real-time timeseries data plotting.

---

## Repository Structure

```
LiveMapWeb/
├── TrajPlot/
│   ├── index.html          # Web interface for trajectory visualization
│   ├── PI_TrajPlot.py      # X-Plane plugin - sends position data via UDP
│   └── server.py           # HTTP/UDP server for TrajPlot
├── FlightPlot/
│   └── PI_FlightPlot.py    # X-Plane plugin - real-time flight parameter plotting
└── README.md               # This file
```

---

## Plugins

### 1. **TrajPlot** - Real-Time Aircraft Trajectory Tracking
Track your X-Plane aircraft position on an interactive web map with trajectory history visualization.

**Files:**
- [`PI_TrajPlot.py`](TrajPlot/PI_TrajPlot.py) - X-Plane plugin (sends position data via UDP)
- [`server.py`](TrajPlot/server.py) - HTTP/UDP server
- [`index.html`](TrajPlot/index.html) - Web interface

**Features:**
- Live aircraft marker on OpenStreetMap
- Flight trajectory trail (red polyline)
- Real-time position updates (1/second from X-Plane, 2/second web refresh)
- Manual map controls (zoom/pan - no auto-centering)
- Responsive web interface using Leaflet.js

**Monitored Data:**
- Latitude & Longitude
- Altitude (MSL)
- Heading (yaw angle)

**Setup:**
```bash
# 1. Place plugin in X-Plane directory
cp TrajPlot/PI_TrajPlot.py /path/to/X-Plane/Resources/plugins/PythonPlugins/

# 2. Start server
cd TrajPlot
python server.py

# 3. Open browser
# Navigate to http://localhost:8000

# 4. In X-Plane, toggle "TrajPlot: ON" in Plugins menu
```
**Sample Picture**

<img width="3840" height="1080" alt="Screenshot (179)" src="https://github.com/user-attachments/assets/c770e25f-bdd3-41b8-8aee-d712ea7dcaee" />

---

### 2. **FlightPlot** - Real-Time Flight Parameter Analysis
Plot flight parameters in real-time with multi-axis visualization and interactive controls.

**Files:**
- [`PI_FlightPlot.py`](FlightPlot/PI_FlightPlot.py) - X-Plane plugin with PyQt5 GUI

**Features:**
- Multi-parameter synchronized plotting on single time axis
- Independent Y-axes for each parameter (color-coded)
- Real-time data collection from X-Plane datarefs
- Pause/Resume functionality
- Reset data button
- Customizable parameter selection via checkboxes
- Dark theme UI with professional styling
- Automatic Y-axis scaling per parameter
- Real-time on-screen indicator while plotting

**Monitored Parameters:**
- **ALT** - Pressure Altitude (ft)
- **CAS** - Calibrated Airspeed (knots)
- **PTCH** - Pitch angle (degrees)
- **ROLL** - Roll angle (degrees)
- **VSPD** - Vertical Speed (ft/min)

**Setup:**
```bash
# 1. Install dependencies
pip install PyQt5 pyqtgraph

# 2. Place plugin in X-Plane directory
cp FlightPlot/PI_FlightPlot.py /path/to/X-Plane/Resources/plugins/PythonPlugins/

# 3. In X-Plane, toggle "FlightPlot: Toggle: ON" in Plugins menu
# PyQt5 window will open automatically
```
**Sample Picture**

<img width="3840" height="1080" alt="Screenshot (180)" src="https://github.com/user-attachments/assets/74fdb77e-cc3d-4528-8463-f1c3c0de2975" />

---

## Requirements

### All Plugins
- **X-Plane 11+** with XPPython3 installed
- **Python 3.6+**

### TrajPlot
- Python standard library: `socket`, `json`, `http.server`, `threading`
- Modern web browser (Chrome, Firefox, Edge, Safari)
- Internet connection (for OpenStreetMap tiles)

### FlightPlot
- **PyQt5**: `pip install PyQt5`
- **pyqtgraph**: `pip install pyqtgraph`

---

## Installation

### Quick Start

#### 1. Install XPPython3
Follow [XPPython3 documentation](https://xppython3.readthedocs.io/) for your X-Plane version.

#### 2. Install Python Dependencies
```bash
pip install PyQt5 pyqtgraph
```

#### 3. Copy Plugins to X-Plane

**Windows:**
```bash
copy TrajPlot\PI_TrajPlot.py "C:\X-Plane 11\Resources\plugins\PythonPlugins\"
copy FlightPlot\PI_FlightPlot.py "C:\X-Plane 11\Resources\plugins\PythonPlugins\"
```

**Linux/macOS:**
```bash
cp TrajPlot/PI_TrajPlot.py ~/X-Plane\ 11/Resources/plugins/PythonPlugins/
cp FlightPlot/PI_FlightPlot.py ~/X-Plane\ 11/Resources/plugins/PythonPlugins/
```

#### 4. Start TrajPlot Server (if using TrajPlot)
```bash
cd TrajPlot
python server.py
```

---

## Usage

### TrajPlot - Trajectory Visualization
1. Start [`TrajPlot/server.py`](TrajPlot/server.py)
2. Open `http://localhost:8000` in your web browser
3. Start X-Plane and load a flight
4. Toggle **Plugins → LiveMap → Toggle LiveMap: ON**
5. Aircraft marker appears on map with trajectory trail updating in real-time
6. Use map controls to zoom and pan

### FlightPlot - Parameter Analysis
1. Start X-Plane and load a flight
2. Toggle **Plugins → FlightPlot → Toggle: ON**
3. PyQt5 plotting window opens automatically
4. Select parameters to display by checking parameter checkboxes
5. Monitor real-time flight data
6. Use **Pause** button to freeze the plot
7. Use **Reset** button to clear data and start fresh

---

## Adding New Plugins

To extend LiveMapWeb with new plugins:

1. Create a new directory: `mkdir NewPlugin`
2. Add your X-Plane Python plugin file(s)
3. Update this README with:
   - Plugin description and purpose
   - File listing with descriptions
   - Features and monitored parameters
   - Setup and installation instructions
   - Python dependencies

**Plugin Template Structure:**
```
NewPlugin/
├── PI_NewPlugin.py       # Main X-Plane plugin file
├── server.py             # (optional) HTTP/UDP server if web component needed
├── index.html            # (optional) Web UI if applicable
└── requirements.txt      # (optional) Python dependencies list
```

---

## Technical Details

### Data Communication
- **TrajPlot**: X-Plane plugin reads datarefs → UDP JSON packets (port 49005) → HTTP server serves `/data` endpoint → Web client fetches updates
- **FlightPlot**: X-Plane plugin reads datarefs → Data queued in thread-safe queue → PyQt5 thread consumes queue → Plot updates

### Update Rates
- **TrajPlot**: 
  - X-Plane plugin: ~1 Hz (1 second flight loop callback)
  - Web client: 2 Hz (500ms refresh interval)
- **FlightPlot**: 
  - X-Plane plugin: 1 Hz data collection
  - Plot refresh: 5 Hz (200ms timer)
  - Maximum data points: 14,400 (4 hours at 1 Hz)

### Datarefs Used

| Plugin | Dataref | Purpose | Range |
|--------|---------|---------|-------|
| TrajPlot | `sim/flightmodel/position/latitude` | Aircraft latitude | ±90° |
| TrajPlot | `sim/flightmodel/position/longitude` | Aircraft longitude | ±180° |
| TrajPlot | `sim/flightmodel/position/elevation` | Altitude MSL | feet |
| TrajPlot | `sim/flightmodel/position/psi` | Heading/Yaw | 0-360° |
| FlightPlot | `sim/flightmodel2/position/pressure_altitude` | Pressure altitude | feet |
| FlightPlot | `sim/cockpit2/gauges/indicators/airspeed_kts_pilot` | Airspeed | knots |
| FlightPlot | `sim/flightmodel/position/theta` | Pitch | ±90° |
| FlightPlot | `sim/flightmodel/position/phi` | Roll | ±180° |
| FlightPlot | `sim/cockpit2/gauges/indicators/vvi_fpm_pilot` | Vertical speed | ft/min |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Plugins not appearing in X-Plane | Ensure XPPython3 is installed; check X-Plane logs (`Log.txt`) |
| TrajPlot: No map data appearing | Verify [`TrajPlot/server.py`](TrajPlot/server.py) is running; check UDP port 49005 is not blocked |
| TrajPlot: Connection refused on localhost:8000 | Check if port 8000 is in use; try different port in server.py |
| FlightPlot: PyQt5 window won't open | Install PyQt5/pyqtgraph: `pip install PyQt5 pyqtgraph`; check Python version (3.6+) |
| ModuleNotFoundError | Install missing dependencies: `pip install PyQt5 pyqtgraph` |
| Data not updating | Verify plugin is enabled in X-Plane Plugins menu; check X-Plane is in active flight |

---

## Performance Notes

- **TrajPlot trajectory trail** stores all points in browser memory (resets on page refresh)
- **FlightPlot data buffer** limited to 14,400 points to prevent memory issues
- Network latency between X-Plane and server may cause slight delays
- Web map performance depends on browser and number of trajectory points

---

## Authors
- **Vyom Shukla** - TrajPlot, FlightPlot plugins

---

## Future Enhancements
- [ ] Data export to CSV/JSON format
- [ ] Flight recording and playback functionality
- [ ] Multi-aircraft tracking support
- [ ] Additional flight parameters (fuel, engines, systems)
- [ ] Performance optimization for long flights
- [ ] Integration with real-world flight data
- [ ] Mobile-friendly responsive design
- [ ] Cloud synchronization
- [ ] Advanced analytics and statistics
- [ ] Custom parameter plotting
