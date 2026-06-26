# sim/plant_simulator.py (Final Production Edition)
import asyncio
import struct
import logging
import random
import threading
import queue
import math
import tkinter as tk
from tkinter import font
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusServerContext, ModbusSlaveContext
from pymodbus.server import ModbusTcpServer

# Suppress standard logging to keep the terminal completely clean for input()
logging.basicConfig(level=logging.WARNING, format="%(asctime)s [Plant] %(message)s")
log = logging.getLogger("plant")

HOST = "0.0.0.0"
PORT = 5020

def float_to_regs(value: float) -> list:
    packed = struct.pack(">f", float(value))
    return list(struct.unpack(">HH", packed))

def regs_to_float(regs: list) -> float:
    return struct.unpack(">f", struct.pack(">HH", regs[0], regs[1]))[0]

class PlantModel:
    def __init__(self):
        # True physical state
        self.true_temp = 21.0
        self.true_level = 2.0
        self.true_pressure = 4.0
        self.true_ph = 7.0
        self.true_turb = 5.0
        self.true_flow = 0.0

        # Noisy state (What the PLC actually reads) - Initialized to prevent GUI crashes
        self.noisy_temp = 21.0
        self.noisy_level = 2.0
        self.noisy_pressure = 4.0
        self.noisy_ph = 7.0
        self.noisy_turb = 5.0
        self.noisy_flow = 0.0

        # Actuator states (Read from PLC)
        self.inlet_valve_open = False
        self.cooling_pump_on = False
        self.dosing_pump_on = False
        self.outlet_pump_on = False

        # Fault Injection State
        self.faults = {'temp': None, 'level': None, 'pressure': None, 'ph': None, 'turb': None}
        self.network_connected = True

    def inject_fault(self, sensor, fault_type):
        self.faults[sensor] = fault_type
        print(f"⚠️ FAULT INJECTED: {sensor} -> {fault_type}")

    def clear_faults(self):
        self.faults = {k: None for k in self.faults}
        print("✅ All sensor faults cleared.")

    def step(self, dt_s: float):
        if not self.network_connected: return

        # 1. Level & Flow (Inlet Valve @ 0x0020, Outlet @ 0x0026)
        inflow = 0.05 if self.inlet_valve_open else 0.0
        # Outlet flow depends on tank pressure (sqrt of level)
        outflow = 0.0
        if self.outlet_pump_on and self.true_level > 0.05:
            outflow = 0.04 * math.sqrt(max(0.1, self.true_level))
        
        self.true_flow = (inflow * 60.0) * 10.0 # Simulate LPM
        self.true_level += (inflow - outflow) * dt_s
        self.true_level = max(0.0, min(4.0, self.true_level))

        # 2. Temperature (Cooling Pump @ 0x0022)
        # Simulate a process heater always ON
        heat_in = 0.15 * dt_s 
        cool_out = 0.4 * dt_s if self.cooling_pump_on else 0.0
        self.true_temp += (heat_in - cool_out)
        self.true_temp = max(5.0, min(120.0, self.true_temp))

        # 3. Pressure (Dosing/Relief Pump @ 0x0024)
        press_build = 0.1 * dt_s
        press_relief = 0.5 * dt_s if self.dosing_pump_on else 0.0
        self.true_pressure += (press_build - press_relief)
        self.true_pressure = max(0.0, min(15.0, self.true_pressure))

        # 4. pH & Turbidity
        ph_drift = -0.02 * dt_s
        ph_dose = 0.1 * dt_s if self.dosing_pump_on else 0.0
        self.true_ph = max(2.0, min(12.0, self.true_ph + ph_drift + ph_dose))

        turb_gen = 0.5 * dt_s if self.inlet_valve_open else -0.1 * dt_s
        self.true_turb = max(0.1, min(100.0, self.true_turb + turb_gen))

        # 5. Apply Micro-Noise (±0.01) to mimic real analog sensors without triggering false alarms
        self.noisy_temp = self._apply_fault('temp', self.true_temp + random.uniform(-0.01, 0.01))
        self.noisy_level = self._apply_fault('level', self.true_level + random.uniform(-0.005, 0.005))
        self.noisy_pressure = self._apply_fault('pressure', self.true_pressure + random.uniform(-0.01, 0.01))
        self.noisy_ph = self._apply_fault('ph', self.true_ph + random.uniform(-0.01, 0.01))
        self.noisy_turb = self._apply_fault('turb', self.true_turb + random.uniform(-0.1, 0.1))
        self.noisy_flow = self.true_flow + random.uniform(-0.5, 0.5)

    def _apply_fault(self, sensor, normal_val):
        fault = self.faults.get(sensor)
        if fault == 'stuck': return 25.0 if sensor == 'temp' else 2.0
        if fault == 'oor_high': return 150.0 if sensor == 'temp' else 12.0
        if fault == 'oor_low': return -10.0 if sensor == 'temp' else -1.0
        return round(normal_val, 2)

# ── Tkinter GUI Dashboard ─────────────────────────────────────────
class DashboardWindow:
    def __init__(self, root, model):
        self.root = root
        self.model = model
        self.root.title("🏭 Mizan Digital Twin - Live SCADA")
        self.root.geometry("480x620")
        self.root.configure(bg="#121212")
        self.root.resizable(False, False)
        
        title_font = font.Font(family="Helvetica", size=16, weight="bold")
        header_font = font.Font(family="Helvetica", size=12, weight="bold")
        text_font = font.Font(family="Consolas", size=11)
        
        tk.Label(root, text="MIZAN DIGITAL TWIN", bg="#121212", fg="#00ff00", font=title_font).pack(pady=10)
        
        # Sensors Frame
        sensors_frame = tk.LabelFrame(root, text=" 📡 Sensor Readings (Clean Analog) ", bg="#1e1e1e", fg="#ffffff", font=header_font, padx=10, pady=10)
        sensors_frame.pack(fill="x", padx=20, pady=10)
        
        self.lbl_temp = tk.Label(sensors_frame, text="Temperature : -- °C", bg="#1e1e1e", fg="#ffffff", font=text_font, anchor="w")
        self.lbl_temp.pack(fill="x", pady=2)
        self.lbl_level = tk.Label(sensors_frame, text="Level       : -- m", bg="#1e1e1e", fg="#ffffff", font=text_font, anchor="w")
        self.lbl_level.pack(fill="x", pady=2)
        self.lbl_press = tk.Label(sensors_frame, text="Pressure    : -- bar", bg="#1e1e1e", fg="#ffffff", font=text_font, anchor="w")
        self.lbl_press.pack(fill="x", pady=2)
        self.lbl_ph = tk.Label(sensors_frame, text="pH          : --", bg="#1e1e1e", fg="#ffffff", font=text_font, anchor="w")
        self.lbl_ph.pack(fill="x", pady=2)
        self.lbl_turb = tk.Label(sensors_frame, text="Turbidity   : -- NTU", bg="#1e1e1e", fg="#ffffff", font=text_font, anchor="w")
        self.lbl_turb.pack(fill="x", pady=2)
        self.lbl_flow = tk.Label(sensors_frame, text="Flow        : -- LPM", bg="#1e1e1e", fg="#ffffff", font=text_font, anchor="w")
        self.lbl_flow.pack(fill="x", pady=2)
        
        # Actuators Frame
        act_frame = tk.LabelFrame(root, text=" ⚙️ Actuator Commands (PLC Output) ", bg="#1e1e1e", fg="#ffffff", font=header_font, padx=10, pady=10)
        act_frame.pack(fill="x", padx=20, pady=10)
        
        self.btn_valve = tk.Label(act_frame, text="Inlet Valve (0x0020)  [ CLOSED ]", bg="#4a0000", fg="#ffffff", font=text_font, anchor="c", relief="raised", padx=5, pady=5)
        self.btn_valve.pack(fill="x", pady=4)
        self.btn_cool = tk.Label(act_frame, text="Cooling Pump (0x0022) [ OFF ]", bg="#00004a", fg="#ffffff", font=text_font, anchor="c", relief="raised", padx=5, pady=5)
        self.btn_cool.pack(fill="x", pady=4)
        self.btn_dose = tk.Label(act_frame, text="Relief Pump (0x0024)  [ OFF ]", bg="#4a4a00", fg="#ffffff", font=text_font, anchor="c", relief="raised", padx=5, pady=5)
        self.btn_dose.pack(fill="x", pady=4)
        self.btn_out = tk.Label(act_frame, text="Outlet Pump (0x0026)  [ OFF ]", bg="#2a2a2a", fg="#ffffff", font=text_font, anchor="c", relief="raised", padx=5, pady=5)
        self.btn_out.pack(fill="x", pady=4)
        
        self.update_ui()

    def update_ui(self):
        m = self.model
        # Sensors
        t_color = "#ff4444" if m.noisy_temp > 90 else "#ffffff"
        self.lbl_temp.config(text=f"Temperature : {m.noisy_temp:5.1f} °C  {'(HIGH!)' if m.noisy_temp > 90 else ''}", fg=t_color)
        
        l_color = "#ff4444" if m.noisy_level < 1.5 else "#ffffff"
        self.lbl_level.config(text=f"Level       : {m.noisy_level:5.2f} m   {'(LOW!)' if m.noisy_level < 1.5 else ''}", fg=l_color)
        
        p_color = "#ff4444" if m.noisy_pressure > 8.0 else "#ffffff"
        self.lbl_press.config(text=f"Pressure    : {m.noisy_pressure:5.2f} bar {'(CRITICAL!)' if m.noisy_pressure > 8.0 else ''}", fg=p_color)
        
        ph_color = "#ffaa00" if not (6.5 <= m.noisy_ph <= 7.5) else "#ffffff"
        self.lbl_ph.config(text=f"pH          : {m.noisy_ph:5.1f}      {'(UNBALANCED)' if not (6.5 <= m.noisy_ph <= 7.5) else ''}", fg=ph_color)
        
        self.lbl_turb.config(text=f"Turbidity   : {m.noisy_turb:5.1f} NTU")
        self.lbl_flow.config(text=f"Flow        : {m.noisy_flow:5.1f} LPM")
        
        # Actuators
        self._update_btn(self.btn_valve, m.inlet_valve_open, "Inlet Valve (0x0020)", "OPEN", "CLOSED", "#005500", "#4a0000")
        self._update_btn(self.btn_cool, m.cooling_pump_on, "Cooling Pump (0x0022)", "ON", "OFF", "#000088", "#00004a")
        self._update_btn(self.btn_dose, m.dosing_pump_on, "Relief Pump (0x0024)", "ON", "OFF", "#888800", "#4a4a00")
        self._update_btn(self.btn_out, m.outlet_pump_on, "Outlet Pump (0x0026)", "ON", "OFF", "#555555", "#2a2a2a")
            
        self.root.after(200, self.update_ui) # 5Hz UI refresh

    def _update_btn(self, btn, state, name, on_txt, off_txt, on_bg, off_bg):
        if state:
            btn.config(text=f"{name} [ {on_txt} ]", bg=on_bg)
        else:
            btn.config(text=f"{name} [ {off_txt} ]", bg=off_bg)

# ── Interactive CLI Thread ─────────────────────────────────────────
def cli_listener(cmd_queue: queue.Queue, model: PlantModel):
    print("\n" + "="*60)
    print("🎮 DIGITAL TWIN CONTROL PANEL")
    print("="*60)
    print("Commands:")
    print("  set temp <val>     - e.g., set temp 105")
    print("  set level <val>    - e.g., set level 1.0")
    print("  set pressure <val> - e.g., set pressure 9.5")
    print("  set ph <val>       - e.g., set ph 4.0")
    print("  fault <sensor> stuck|oor_high|oor_low")
    print("  clear_faults       - Restore all sensors")
    print("  disconnect         - Simulate network drop")
    print("  reconnect          - Restore network")
    print("="*60 + "\n")
    
    while True:
        try:
            cmd = input("🔧 Plant CMD > ").strip().lower()
            cmd_queue.put(cmd)
        except EOFError:
            break

async def process_commands(cmd_queue: queue.Queue, model: PlantModel):
    while True:
        try:
            cmd = cmd_queue.get_nowait()
            parts = cmd.split()
            
            if cmd.startswith("set ") and len(parts) == 3:
                target, val = parts[1], float(parts[2])
                if target == "temp": model.true_temp = val; print(f"🎮 Temp set to {val}°C (Physics will continue from here)")
                elif target == "level": model.true_level = val; print(f"🎮 Level set to {val}m")
                elif target == "pressure": model.true_pressure = val; print(f"🎮 Pressure set to {val} bar")
                elif target == "ph": model.true_ph = val; print(f"🎮 pH set to {val}")
                else: print("❓ Unknown sensor. Try: temp, level, pressure, ph")
            elif cmd.startswith("fault") and len(parts) >= 3:
                sensor, f_type = parts[1], parts[2]
                if sensor in model.faults: model.inject_fault(sensor, f_type)
                else: print(f"❓ Unknown sensor. Try: temp, level, pressure, ph, turb")
            elif cmd == "clear_faults":
                model.clear_faults()
            elif cmd == "disconnect":
                model.network_connected = False
                print("🔌 NETWORK DISCONNECTED")
            elif cmd == "reconnect":
                model.network_connected = True
                print("🔌 NETWORK RECONNECTED")
            else:
                print("❓ Unknown command.")
        except queue.Empty:
            pass
        except ValueError:
            print("❓ Invalid number format.")
        await asyncio.sleep(0.1)

async def plant_loop(slave_ctx: ModbusSlaveContext, model: PlantModel):
    while True:
        await asyncio.sleep(0.5) # 2Hz physics update for smooth visuals
        model.step(dt_s=0.5)
        
        if model.network_connected:
            # Write NOISY sensor data to Modbus (What the PLC actually sees)
            slave_ctx.setValues(3, 0,  float_to_regs(model.noisy_level))     # 0x0000 Level
            slave_ctx.setValues(3, 2,  float_to_regs(model.noisy_pressure))  # 0x0002 Pressure
            slave_ctx.setValues(3, 4,  float_to_regs(model.noisy_ph))        # 0x0004 pH
            slave_ctx.setValues(3, 6,  float_to_regs(model.noisy_flow))      # 0x0006 Flow
            slave_ctx.setValues(3, 8,  float_to_regs(model.noisy_temp))      # 0x0008 Temp
            
            # Read Actuator Commands from PLC
            model.inlet_valve_open = regs_to_float(slave_ctx.getValues(3, 32, 2)) >= 0.5  # 0x0020
            model.cooling_pump_on  = regs_to_float(slave_ctx.getValues(3, 34, 2)) >= 0.5  # 0x0022
            model.dosing_pump_on   = regs_to_float(slave_ctx.getValues(3, 36, 2)) >= 0.5  # 0x0024
            model.outlet_pump_on   = regs_to_float(slave_ctx.getValues(3, 38, 2)) >= 0.5  # 0x0026
        else:
            # Simulate network drop (Sensors read 0.0)
            for i in range(0, 10, 2): slave_ctx.setValues(3, i, [0,0])

# ✅ FIX: Instantiate ModbusTcpServer INSIDE the running event loop
def start_asyncio_server(model, cmd_queue):
    async def run():
        slave_ctx = ModbusSlaveContext(hr=ModbusSequentialDataBlock(0, [0] * 200))
        server_ctx = ModbusServerContext(slaves=slave_ctx, single=True)
        
        # ✅ ModbusTcpServer in pymodbus 3.x requires an active event loop to be instantiated
        server = ModbusTcpServer(context=server_ctx, address=(HOST, PORT))
        
        await asyncio.gather(
            plant_loop(slave_ctx, model),
            process_commands(cmd_queue, model),
            server.serve_forever()
        )
    asyncio.run(run())

def main():
    model = PlantModel()
    cmd_queue = queue.Queue()
    
    # Start Asyncio Modbus Server & CLI Processor in a background thread
    threading.Thread(target=start_asyncio_server, args=(model, cmd_queue), daemon=True).start()
    
    # Start CLI Listener in a background thread
    threading.Thread(target=cli_listener, args=(cmd_queue, model), daemon=True).start()
    
    # Run Tkinter GUI in the main thread (Required for Windows stability)
    root = tk.Tk()
    DashboardWindow(root, model)
    root.mainloop()

if __name__ == "__main__":
    main()