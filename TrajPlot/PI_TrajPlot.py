from XPPython3 import xp
import socket
import json


class PythonInterface:

    def __init__(self):
        self.Name = "TrajPlot"
        self.Sig = "vyomshukla.plugin.trajplot"
        self.Desc = "Sends aircraft lat/lon/alt/heading via UDP"

        self.enabled = True
        self.sock = None
        self.menu_id = None
        self.menu_item = None

        self.dr_lat = None
        self.dr_lon = None
        self.dr_alt = None
        self.dr_head = None

    # ===================================================
    # Plugin start
    # ===================================================
    def XPluginStart(self):

        # UDP
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Datarefs
        self.dr_lat = xp.findDataRef("sim/flightmodel/position/latitude")
        self.dr_lon = xp.findDataRef("sim/flightmodel/position/longitude")
        self.dr_alt = xp.findDataRef("sim/flightmodel/position/elevation")
        self.dr_head = xp.findDataRef("sim/flightmodel/position/psi")

        # ================================
        # Create menu in Plugins menu
        # ================================
        parent_menu = xp.findPluginsMenu()  # valid in your version
        item_ref = xp.appendMenuItem(parent_menu, "TrajPlot", 0)

        self.menu_id = xp.createMenu(
            "TrajPlot",
            parent_menu,
            item_ref,
            self.menuHandler,
            0
        )

        self.menu_item = xp.appendMenuItem(self.menu_id, "Toggle TrajPlot: ON", 0)

        # Register callback
        xp.registerFlightLoopCallback(self.flightLoopCB, 1.0, 0)

        xp.log("[TrajPlot] Started successfully")

        return self.Name, self.Sig, self.Desc

    # ===================================================
    def XPluginEnable(self):
        return 1

    def XPluginDisable(self):
        xp.unregisterFlightLoopCallback(self.flightLoopCB, 0)

    def XPluginStop(self):
        if self.sock:
            self.sock.close()

    def XPluginReceiveMessage(self, inFromWho, inMessage, inParam):
        pass

    # ===================================================
    # Menu handler
    # ===================================================
    def menuHandler(self, menuRef, itemRef):

        self.enabled = not self.enabled
        next_state = "OFF" if self.enabled else "ON"

        xp.setMenuItemName(self.menu_id, self.menu_item, f"Toggle TrajPlot: {next_state}")

        if self.enabled:
            xp.registerFlightLoopCallback(self.flightLoopCB, 1.0, 0)
            xp.log("[TrajPlot] Enabled")
        else:
            try:
                xp.unregisterFlightLoopCallback(self.flightLoopCB, 0)
            except:
                pass
            xp.log("[TrajPlot] Disabled")

    # ===================================================
    # Flight Loop
    # ===================================================
    def flightLoopCB(self, elapsed1, elapsed2, counter, refcon):

        if not self.enabled:
            return 1.0

        try:
            lat = xp.getDatad(self.dr_lat)
            lon = xp.getDatad(self.dr_lon)
            alt = xp.getDatad(self.dr_alt)
            head = xp.getDatad(self.dr_head)

            pkt = {
                "lat": lat,
                "lon": lon,
                "alt": alt,
                "heading": head
            }

            self.sock.sendto(json.dumps(pkt).encode(), ("127.0.0.1", 49005))

        except Exception as e:from XPPython3 import xp
import socket
import json


class PythonInterface:

    def __init__(self):
        self.Name = "TrajPlot"
        self.Sig = "vyomshukla.plugin.trajplot"
        self.Desc = "Sends aircraft lat/lon/alt/heading via UDP"

        self.enabled = False  # Plugin starts OFF by default
        self.sock = None
        self.menu_id = None
        self.menu_item = None

        self.dr_lat = None
        self.dr_lon = None
        self.dr_alt = None
        self.dr_head = None

    def XPluginStart(self):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Datarefs
        self.dr_lat = xp.findDataRef("sim/flightmodel/position/latitude")
        self.dr_lon = xp.findDataRef("sim/flightmodel/position/longitude")
        self.dr_alt = xp.findDataRef("sim/flightmodel/position/elevation")
        self.dr_head = xp.findDataRef("sim/flightmodel/position/psi")

        # Menu
        parent_menu = xp.findPluginsMenu()
        item_ref = xp.appendMenuItem(parent_menu, "TrajPlot", 0)

        self.menu_id = xp.createMenu(
            "TrajPlot", parent_menu, item_ref, self.menuHandler, 0
        )

        # Plugin starts OFF → menu should show "Toggle: ON"
        self.menu_item = xp.appendMenuItem(
            self.menu_id, "Toggle: ON", 0
        )

        xp.log("[TrajPlot] Loaded (OFF by default)")

        # Send initial OFF status
        try:
            self.sock.sendto(json.dumps({"status": "OFF"}).encode(), ("127.0.0.1", 49005))
        except:
            pass

        return self.Name, self.Sig, self.Desc

    def XPluginEnable(self):
        return 1

    def XPluginDisable(self):
        try:
            xp.unregisterFlightLoopCallback(self.flightLoopCB, 0)
        except:
            pass
        return 1

    def XPluginStop(self):
        try:
            self.sock.sendto(json.dumps({"status": "OFF"}).encode(), ("127.0.0.1", 49005))
        except:
            pass

        if self.sock:
            self.sock.close()

    # ========== MENU HANDLER ==========
    def menuHandler(self, menuRef, itemRef):

        # Flip ON/OFF
        self.enabled = not self.enabled

        if self.enabled:
            # Plugin turned ON → show "Toggle: OFF"
            xp.setMenuItemName(self.menu_id, self.menu_item, "Toggle: OFF")

            xp.registerFlightLoopCallback(self.flightLoopCB, 1.0, 0)
            xp.log("[TrajPlot] Enabled")

        else:
            # Plugin turned OFF → show "Toggle: ON"
            xp.setMenuItemName(self.menu_id, self.menu_item, "Toggle: ON")

            try:
                xp.unregisterFlightLoopCallback(self.flightLoopCB, 0)
            except:
                pass

            # Let server know plugin is OFF
            try:
                self.sock.sendto(json.dumps({"status": "OFF"}).encode(), ("127.0.0.1", 49005))
            except:
                pass

            xp.log("[TrajPlot] Disabled")

    # ========== FLIGHT LOOP ==========
    def flightLoopCB(self, elapsed1, elapsed2, counter, refcon):

        # Safety check
        if not self.enabled:
            return 1.0

        try:
            pkt = {
                "lat": xp.getDatad(self.dr_lat),
                "lon": xp.getDatad(self.dr_lon),
                "alt": xp.getDatad(self.dr_alt),
                "heading": xp.getDatad(self.dr_head),
                "status": "ON"
            }

            self.sock.sendto(json.dumps(pkt).encode(), ("127.0.0.1", 49005))

        except Exception as e:
            xp.log(f"[TrajPlot] ERROR: {e}")

        return 1.0

            xp.log(f"[TrajPlot] ERROR: {e}")

        return 1.0
