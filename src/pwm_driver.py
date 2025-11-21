# src/pwm_driver.py
import os
import time

class SysfsPWM:
    def __init__(self, pwmchip=0, channel=0, frequency_hz=1000, wait_export=0.1):
        self.pwmchip = pwmchip
        self.channel = channel
        self.base = f"/sys/class/pwm/pwmchip{self.pwmchip}"
        self.pwm_path = f"{self.base}/pwm{self.channel}"
        self.frequency = frequency_hz
        self.period_ns = int(1e9 / float(self.frequency))
        if not os.path.isdir(self.base):
            raise RuntimeError(f"PWM base {self.base} no existe. Comprueba Device Tree / drivers.")
        self._export(wait_export)
        self._configure()

    def _write(self, path, value):
        with open(path, "w") as f:
            f.write(str(value))

    def _export(self, wait):
        if not os.path.isdir(self.pwm_path):
            self._write(os.path.join(self.base, "export"), self.channel)
            time.sleep(wait)
            if not os.path.isdir(self.pwm_path):
                raise RuntimeError(f"No se creó {self.pwm_path} tras export; revisar permisos o driver.")

    def _configure(self):
        # disable before change
        try:
            self._write(os.path.join(self.pwm_path, "enable"), 0)
        except Exception:
            pass
        # set period then duty_cycle, then enable
        self._write(os.path.join(self.pwm_path, "period"), self.period_ns)
        self._write(os.path.join(self.pwm_path, "duty_cycle"), 0)
        self._write(os.path.join(self.pwm_path, "enable"), 1)

    def set_duty_percent(self, percent):
        if percent < 0: percent = 0
        if percent > 100: percent = 100
        duty = int(self.period_ns * (percent / 100.0))
        self._write(os.path.join(self.pwm_path, "duty_cycle"), duty)

    def disable(self):
        self._write(os.path.join(self.pwm_path, "enable"), 0)

if __name__ == "__main__":
    p = SysfsPWM(pwmchip=0, channel=0, frequency_hz=500)
    try:
        for i in range(0, 101, 5):
            p.set_duty_percent(i)
            time.sleep(0.05)
    finally:
        p.disable()
