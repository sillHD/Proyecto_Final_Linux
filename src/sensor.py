# src/sensor.py
import time
from smbus2 import SMBus

class BH1750:
    # Direcciones posibles: 0x23 (default) o 0x5C
    DEFAULT_ADDR = 0x23
    CMD_POWER_ON = 0x01
    CMD_RESET = 0x07
    CMD_CONT_H_RES = 0x10

    def __init__(self, i2c_bus=0, address=DEFAULT_ADDR):
        self.address = address
        self.bus_num = i2c_bus
        self.bus = SMBus(self.bus_num)
        self._init_sensor()

    def _init_sensor(self):
        try:
            # power on
            self.bus.write_byte(self.address, self.CMD_POWER_ON)
            time.sleep(0.01)
            # reset
            self.bus.write_byte(self.address, self.CMD_RESET)
            time.sleep(0.01)
            # continuous high resolution
            self.bus.write_byte(self.address, self.CMD_CONT_H_RES)
            time.sleep(0.18)  # espera lecturas estables
        except Exception as e:
            raise RuntimeError(f"BH1750 init error (I2C bus {self.bus_num} addr {hex(self.address)}): {e}")

    def read_lux(self):
        try:
            data = self.bus.read_i2c_block_data(self.address, self.CMD_CONT_H_RES, 2)
            raw = (data[0] << 8) | data[1]
            lux = raw / 1.2
            return lux
        except Exception as e:
            # No aborta el programa: devuelve -1 para indicar error de lectura
            print(f"[sensor.BH1750] read error: {e}")
            return -1.0

if __name__ == "__main__":
    s = BH1750(i2c_bus=0)
    while True:
        print("Lux:", s.read_lux())
        time.sleep(0.5)
