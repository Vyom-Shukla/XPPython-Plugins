## Overview
**LiveMapWeb** is a comprehensive X-Plane plugin ecosystem for real-time data visualization. It provides multiple tools for monitoring and analyzing flight data, including live aircraft tracking and timeseries data plotting.

---

## Repository Structure

```
LiveMapWeb/
├── LiveMap/
│   ├── index.html          # Web interface for aircraft tracking
│   ├── PI_LiveMap.py       # X-Plane plugin - sends position data
│   └── server.py           # HTTP/UDP server for LiveMap
├── ParaViz/
│   └── PI_ParaViz.py       # X-Plane plugin - real-time data plotting
└── README.md               # This file
```

---

## Plugins

### 1. **LiveMap** - Real-Time Aircraft Tracking
Track your X-Plane aircraft position on an interactive web map.

**Files:**
- `PI_LiveMap.py` - X-Plane plugin
- `server.py` - Web server (HTTP + UDP)
- `index.html` - Web interface

**Features:**
- Live aircraft marker on OpenStreetMap
- Flight trail visualization
- Real-time position updates (1/second from X-Plane, 2/second web refresh)
- Manual map controls (zoom/pan)

**Setup:**
```bash
# 1. Place plugin in X-Plane directory
cp LiveMap/PI_LiveMap.py /path/to/X-Plane/Resources/plugins/PythonPlugins/

# 2. Start server
cd LiveMap
python server.py

# 3. Open browser
# Navigate to http://localhost:8000

# 4. In X-Plane, toggle "LiveMap: ON" in Plugins menu
```

---

### 2. **ParaViz** - Real-Time Timeseries Data Plotting
Plot flight parameters (altitude, airspeed, pitch, roll, vertical speed) in real-time.

**Files:**
- `PI_ParaViz.py` - X-Plane plugin with PyQt5 UI

**Features:**
- Multi-parameter plot with synchronized time axis
- Independent Y-axes for each parameter (color-coded)
- Real-time data collection from X-Plane datarefs
- Pause/Resume plotting
- Reset functionality
- Customizable parameter selection
- Dark theme UI

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
cp ParaViz/PI_ParaViz.py /path/to/X-Plane/Resources/plugins/PythonPlugins/

# 3. In X-Plane, toggle "ParaViz: ON" in Plugins menu
# PyQt5 window will open automatically
```

---

## Requirements

### All Plugins
- **X-Plane 11+** with XPPython3 installed
- **Python 3.6+**

### LiveMap
- Python `socket`, `json`, `http.server` (standard library)
- Modern web browser
- Internet connection (for map tiles)

### ParaViz
- **PyQt5**: `pip install PyQt5`
- **pyqtgraph**: `pip install pyqtgraph`

---

## Installation

### 1. Install XPPython3
Follow [XPPython3 documentation](https://xppython3.readthedocs.io/) for your X-Plane version.

### 2. Install Plugin Dependencies
```bash
pip install PyQt5 pyqtgraph
```

### 3. Copy Plugins to X-Plane
```bash
# Linux/Mac
cp LiveMap/PI_LiveMap.py ~/X-Plane\ 11/Resources/plugins/PythonPlugins/
cp ParaViz/PI_ParaViz.py ~/X-Plane\ 11/Resources/plugins/PythonPlugins/

# Windows
copy LiveMap\PI_LiveMap.py "C:\X-Plane 11\Resources\plugins\PythonPlugins\"
copy ParaViz\PI_ParaViz.py "C:\X-Plane 11\Resources\plugins\PythonPlugins\"
```

### 4. Start LiveMap Server (if using LiveMap)
```bash
cd LiveMap
python server.py
```

---

## Usage

### LiveMap
1. Start server.py
2. Open `http://localhost:8000` in browser
3. Start X-Plane flight
4. Toggle **Plugins → LiveMap → Toggle LiveMap: ON**
5. Aircraft marker appears on map with trail

### ParaViz
1. Start X-Plane flight
2. Toggle **Plugins → ParaViz → Toggle: ON**
3. PyQt5 window opens with live plot
4. Check parameters to display
5. Use **Pause** to freeze plot, **Reset** to clear data

---

## Adding New Plugins

To add a new plugin to this repository:

1. Create a new directory: `mkdir NewPlugin`
2. Add your X-Plane Python plugin file(s)
3. Update this README with:
   - Plugin description
   - File listing
   - Features & parameters
   - Setup instructions
   - Requirements

**Plugin Template Structure:**
```
NewPlugin/
├── PI_NewPlugin.py       # Main plugin file
├── server.py             # (optional) if web component needed
├── index.html            # (optional) if web UI needed
└── requirements.txt      # (optional) Python dependencies
```

---

## Technical Details

### Data Communication
- **LiveMap**: UDP packets (port 49005) → HTTP JSON responses
- **ParaViz**: Direct X-Plane dataref reads → PyQt5 plotting

### Update Rates
- **LiveMap**: ~1 Hz from X-Plane, 2 Hz web refresh
- **ParaViz**: 200ms plot refresh, real-time data collection

### Datarefs Used
| Plugin | Dataref | Purpose |
|--------|---------|---------|
| LiveMap | `sim/flightmodel/position/latitude` | Aircraft latitude |
| LiveMap | `sim/flightmodel/position/longitude` | Aircraft longitude |
| LiveMap | `sim/flightmodel/position/elevation` | Altitude MSL |
| LiveMap | `sim/flightmodel/position/psi` | Heading |
| ParaViz | `sim/flightmodel2/position/pressure_altitude` | Pressure altitude |
| ParaViz | `sim/cockpit2/gauges/indicators/airspeed_kts_pilot` | Airspeed |
| ParaViz | `sim/flightmodel/position/theta` | Pitch |
| ParaViz | `sim/flightmodel/position/phi` | Roll |
| ParaViz | `sim/cockpit2/gauges/indicators/vvi_fpm_pilot` | Vertical speed |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Plugins not loading | Ensure XPPython3 is installed; check X-Plane logs |
| LiveMap: No data | Check server.py is running; verify UDP port 49005 is open |
| ParaViz: Window won't open | Install PyQt5/pyqtgraph; check Python version compatibility |
| ModuleNotFoundError | Install missing dependencies: `pip install -r requirements.txt` |

---

## Authors
- **Vyom Shukla** - LiveMap & ParaViz plugins

---

## License
Specify your license here (MIT, Apache 2.0, etc.)

---

## Future Enhancements
- [ ] Data export (CSV/JSON)
- [ ] Recording/playback functionality
- [ ] Additional flight parameters
- [ ] Multi-aircraft tracking
- [ ] Performance optimization
