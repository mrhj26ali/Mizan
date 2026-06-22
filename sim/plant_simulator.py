# sim/plant_simulator.py
"""
pymodbus 3.8.1 Modbus TCP server — simulated water treatment plant.
Exposes sensor readings and reads actuator commands from the Mizan runtime.

Register map (holding registers, IEEE-754 float in 2 consecutive 16-bit words,
big-endian ABCD word order — matches mizan_modbus.c):
  0x0000 (0)   level_sensor      متر          (tank water level, 0–4 m)
  0x0002 (2)   turbidity_sensor  NTU
  0x0004 (4)   ph_sensor         لا_وحدة
  0x0006 (6)   flow_sensor       لتر_في_الدقيقة
  0x0008 (8)   temp_sensor       سيلزيوس
  0x0020 (32)  inlet_valve       0/1  (actuator written by Mizan)
  0x0022 (34)  outlet_pump       0/1
  0x0024 (36)  dosing_pump       0/1

Run:
  pip install pymodbus==3.8.1
  python sim/plant_simulator.py
"""

import asyncio
import struct
import logging
import random

from pymodbus.datastore import (
    ModbusSequentialDataBlock,
    ModbusServerContext,
    ModbusSlaveContext,
)
from pymodbus.server import ModbusTcpServer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [Plant] %(message)s"
)
log = logging.getLogger("plant")

HOST = "0.0.0.0"
PORT = 5020


# ── IEEE-754 float <-> two 16-bit registers (big-endian ABCD) ─────────

def float_to_regs(value: float) -> list:
    packed = struct.pack(">f", float(value))
    hi, lo = struct.unpack(">HH", packed)
    return [hi, lo]

def regs_to_float(regs: list) -> float:
    packed = struct.pack(">HH", regs[0], regs[1])
    return struct.unpack(">f", packed)[0]


# ── Physical plant model ─────────────────────────────────────────────

class PlantModel:
    """Simple coupled water-treatment plant model.
    Tank level responds to inlet valve + outlet pump.
    pH drifts acidic and is corrected by dosing pump.
    Turbidity clears when fresh water flows in.
    """

    def __init__(self):
        self.level_m       = 2.0    # starts half-full of a 4 m tank
        self.turbidity_ntu = 8.0
        self.ph            = 7.0
        self.flow_lpm      = 0.0
        self.temp_c        = 21.0

        # actuator states (read back from registers each tick)
        self.inlet_valve_open = False
        self.outlet_pump_on   = False
        self.dosing_pump_on   = False

    def step(self, dt_s: float = 1.0):
        inflow  = 12.0 if self.inlet_valve_open else 0.0
        outflow = 10.0 if self.outlet_pump_on   else 0.0
        self.flow_lpm = inflow

        # Level: convert L/min to m rise in 3 m² cross-section tank
        delta_liters = (inflow - outflow) * (dt_s / 60.0)
        self.level_m += (delta_liters / 1000.0) / 3.0
        self.level_m = max(0.0, min(4.0, self.level_m))

        # Turbidity
        if self.inlet_valve_open:
            self.turbidity_ntu -= 0.15
        self.turbidity_ntu += random.uniform(-0.05, 0.10)
        self.turbidity_ntu = max(0.5, min(50.0, self.turbidity_ntu))

        # pH
        correction = 0.08 if self.dosing_pump_on else -0.01
        self.ph += correction + random.uniform(-0.02, 0.02)
        self.ph = max(4.0, min(10.0, self.ph))

        # Temperature (slow drift)
        self.temp_c += random.uniform(-0.05, 0.05)
        self.temp_c = max(5.0, min(40.0, self.temp_c))


# ── Plant loop — runs every second, independent of PLC poll rate ─────

async def plant_loop(slave_ctx: ModbusSlaveContext, model: PlantModel):
    """Steps the physical model each second and syncs with the Modbus registers."""
    while True:
        await asyncio.sleep(1.0)
        model.step(dt_s=1.0)

        # Write sensor readings into holding registers (fc=3 for ModbusSlaveContext)
        slave_ctx.setValues(3, 0,  float_to_regs(model.level_m))
        slave_ctx.setValues(3, 2,  float_to_regs(model.turbidity_ntu))
        slave_ctx.setValues(3, 4,  float_to_regs(model.ph))
        slave_ctx.setValues(3, 6,  float_to_regs(model.flow_lpm))
        slave_ctx.setValues(3, 8,  float_to_regs(model.temp_c))

        # Read actuator commands that the Mizan binary may have written
        model.inlet_valve_open = regs_to_float(slave_ctx.getValues(3, 32, 2)) >= 0.5
        model.outlet_pump_on   = regs_to_float(slave_ctx.getValues(3, 34, 2)) >= 0.5
        model.dosing_pump_on   = regs_to_float(slave_ctx.getValues(3, 36, 2)) >= 0.5

        log.info(
            f"level={model.level_m:.2f}m  "
            f"turb={model.turbidity_ntu:.1f}NTU  "
            f"pH={model.ph:.2f}  "
            f"temp={model.temp_c:.1f}°C  "
            f"| inlet={'ON' if model.inlet_valve_open else 'off'}  "
            f"pump={'ON' if model.outlet_pump_on else 'off'}  "
            f"dosing={'ON' if model.dosing_pump_on else 'off'}"
        )


# ── Main ─────────────────────────────────────────────────────────────

async def main():
    model = PlantModel()

    # FIX 1: Remove zero_mode=True — not a valid parameter in pymodbus 3.x.
    # ModbusSequentialDataBlock already zero-initializes.
    slave_ctx = ModbusSlaveContext(
        hr=ModbusSequentialDataBlock(0, [0] * 200)
    )
    server_ctx = ModbusServerContext(slaves=slave_ctx, single=True)

    # FIX 2: Use ModbusTcpServer directly (pymodbus 3.x recommended pattern).
    # This avoids the asyncio.create_task ordering issue with StartAsyncTcpServer.
    server = ModbusTcpServer(
        context=server_ctx,
        address=(HOST, PORT),
    )

    log.info(f"🏭 محاكي محطة معالجة المياه — Modbus TCP على {HOST}:{PORT}")
    log.info("   سجلات الحساسات : 0x0000–0x0008 (قراءة)")
    log.info("   سجلات المشغلات: 0x0020–0x0024 (كتابة)")

    # FIX 3: Run plant loop and server concurrently using asyncio.gather.
    # create_task must be called inside a running event loop, which gather ensures.
    await asyncio.gather(
        plant_loop(slave_ctx, model),
        server.serve_forever(),
    )


if __name__ == "__main__":
    asyncio.run(main())