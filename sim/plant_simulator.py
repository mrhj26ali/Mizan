# sim/plant_simulator.py (Interactive Demo Edition)
import asyncio
import struct
import logging
import random
import threading
import queue
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusServerContext, ModbusSlaveContext
from pymodbus.server import ModbusTcpServer

logging.basicConfig(level=logging.INFO, format="%(asctime)s [Plant] %(message)s")
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
        self.level_m, self.turbidity_ntu, self.ph, self.flow_lpm, self.temp_c = 2.0, 8.0, 7.0, 0.0, 21.0
        self.inlet_valve_open, self.outlet_pump_on, self.dosing_pump_on = False, False, False
        self.manual_override = False
        self.network_connected = True

    def step(self, dt_s: float = 1.0):
        if self.manual_override: return # Freeze physics if user is manually controlling
        inflow, outflow = (12.0 if self.inlet_valve_open else 0.0), (10.0 if self.outlet_pump_on else 0.0)
        self.flow_lpm = inflow
        self.level_m += (((inflow - outflow) * (dt_s / 60.0)) / 1000.0) / 3.0
        self.level_m = max(0.0, min(4.0, self.level_m))
        self.turbidity_ntu = max(0.5, min(50.0, self.turbidity_ntu - 0.15 + random.uniform(-0.05, 0.10) if self.inlet_valve_open else self.turbidity_ntu + 0.1))
        self.ph = max(4.0, min(10.0, self.ph + (0.08 if self.dosing_pump_on else -0.01) + random.uniform(-0.02, 0.02)))
        self.temp_c = max(5.0, min(120.0, self.temp_c + random.uniform(-0.05, 0.05)))

# ── Interactive CLI Thread ─────────────────────────────────────────
def cli_listener(cmd_queue: queue.Queue):
    print("\n" + "="*60)
    print("🎮 INTERACTIVE PLANT CONTROL (Demo Mode)")
    print("="*60)
    print("Commands: set level <val> | set temp <val> | disconnect | reconnect | auto")
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
            if cmd.startswith("set level"):
                model.level_m = float(cmd.split()[2]); model.manual_override = True
                log.info(f"🎮 Manual Override: Level set to {model.level_m}m")
            elif cmd.startswith("set temp"):
                model.temp_c = float(cmd.split()[2]); model.manual_override = True
                log.info(f"🎮 Manual Override: Temp set to {model.temp_c}°C")
            elif cmd == "disconnect":
                model.network_connected = False
                log.warning("🔌 NETWORK DISCONNECTED (Simulating cable pull)")
            elif cmd == "reconnect":
                model.network_connected = True
                log.info("🔌 NETWORK RECONNECTED")
            elif cmd == "auto":
                model.manual_override = False
                log.info("🤖 Resuming automatic physics simulation")
            else:
                print("❓ Unknown command.")
        except queue.Empty:
            pass
        await asyncio.sleep(0.1)

async def plant_loop(slave_ctx: ModbusSlaveContext, model: PlantModel):
    while True:
        await asyncio.sleep(1.0)
        model.step(dt_s=1.0)
        
        if model.network_connected:
            slave_ctx.setValues(3, 0,  float_to_regs(model.level_m))
            slave_ctx.setValues(3, 2,  float_to_regs(model.turbidity_ntu))
            slave_ctx.setValues(3, 4,  float_to_regs(model.ph))
            slave_ctx.setValues(3, 6,  float_to_regs(model.flow_lpm))
            slave_ctx.setValues(3, 8,  float_to_regs(model.temp_c))
            
            model.inlet_valve_open = regs_to_float(slave_ctx.getValues(3, 32, 2)) >= 0.5
            model.outlet_pump_on   = regs_to_float(slave_ctx.getValues(3, 34, 2)) >= 0.5
            model.dosing_pump_on   = regs_to_float(slave_ctx.getValues(3, 36, 2)) >= 0.5
        else:
            # If disconnected, return 0.0 to trigger "Disconnect" health rules
            slave_ctx.setValues(3, 0, [0,0]); slave_ctx.setValues(3, 2, [0,0])
            slave_ctx.setValues(3, 4, [0,0]); slave_ctx.setValues(3, 6, [0,0])
            slave_ctx.setValues(3, 8, [0,0])

async def main():
    model = PlantModel()
    slave_ctx = ModbusSlaveContext(hr=ModbusSequentialDataBlock(0, [0] * 200))
    server_ctx = ModbusServerContext(slaves=slave_ctx, single=True)
    server = ModbusTcpServer(context=server_ctx, address=(HOST, PORT))

    log.info(f"🏭 Interactive Plant Simulator running on {HOST}:{PORT}")
    
    cmd_queue = queue.Queue()
    threading.Thread(target=cli_listener, args=(cmd_queue,), daemon=True).start()

    await asyncio.gather(
        plant_loop(slave_ctx, model),
        process_commands(cmd_queue, model),
        server.serve_forever()
    )

if __name__ == "__main__":
    asyncio.run(main())