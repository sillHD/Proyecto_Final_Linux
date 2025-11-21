# src/control_daemon.py
import time
import json
import signal
import threading
import os
from sensor import BH1750
from pwm_driver import SysfsPWM

STATE_FILE = "/tmp/lightcontrol_state.json"
SENSOR_BUS = 0        # normalmente 0 en Lichee; cambia si tu bus es otro
SENSOR_ADDR = 0x23
PWM_CHIP = 0
PWM_CHANNEL = 0
PWM_FREQ = 500        # 500 Hz PWM (ajustable)
SAMPLE_INTERVAL = 0.5 # segundos

class LightDaemon:
    def __init__(self):
        self.sensor = BH1750(i2c_bus=SENSOR_BUS, address=SENSOR_ADDR)
        self.pwm = SysfsPWM(pwmchip=PWM_CHIP, channel=PWM_CHANNEL, frequency_hz=PWM_FREQ)
        self.mode = "auto"         # 'auto' o 'manual'
        self.manual_value = 50.0   # duty % (0-100)
        self.running = False
        self.lock = threading.Lock()
        self._load_state()

    def _load_state(self):
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, "r") as f:
                    s = json.load(f)
                    self.mode = s.get("mode", self.mode)
                    self.manual_value = s.get("manual_value", self.manual_value)
            except Exception:
                print("[daemon] No pude leer state file, usar valores por defecto.")
        else:
            self._save_state()

    def _save_state(self):
        try:
            with open(STATE_FILE, "w") as f:
                json.dump({"mode": self.mode, "manual_value": self.manual_value}, f)
        except Exception as e:
            print(f"[daemon] Error guardando estado: {e}")

    def compute_duty_from_lux(self, lux):
        # mapeo lineal simple: lux 0 -> 100%; lux 1000 -> 0%
        if lux < 0:
            return self.manual_value if self.mode == "manual" else 0
        max_lux = 1000.0
        lux_c = max(0.0, min(lux, max_lux))
        duty = (1.0 - (lux_c / max_lux)) * 100.0
        return max(0.0, min(100.0, duty))

    def step(self):
        lux = self.sensor.read_lux()
        with self.lock:
            if self.mode == "auto":
                duty = self.compute_duty_from_lux(lux)
                self.pwm.set_duty_percent(duty)
                print(f"[daemon] auto | lux={lux:.1f} -> duty={duty:.1f}%")
            else:
                self.pwm.set_duty_percent(self.manual_value)
                print(f"[daemon] manual | duty={self.manual_value}%")
            self._save_state()

    def start(self):
        self.running = True
        def loop():
            while self.running:
                try:
                    self.step()
                except Exception as e:
                    print(f"[daemon] error en step: {e}")
                time.sleep(SAMPLE_INTERVAL)
        self.thread = threading.Thread(target=loop, daemon=True)
        self.thread.start()

    def stop(self):
        print("[daemon] stopping...")
        self.running = False
        try:
            self.pwm.disable()
        except Exception:
            pass

# Entrypoint
if __name__ == "__main__":
    d = LightDaemon()
    def handle_sig(signum, frame):
        d.stop()
        exit(0)
    signal.signal(signal.SIGTERM, handle_sig)
    signal.signal(signal.SIGINT, handle_sig)
    d.start()
    while True:
        time.sleep(1)
