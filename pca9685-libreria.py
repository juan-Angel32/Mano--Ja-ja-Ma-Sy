from machine import SoftI2C
import time

class PCA9685:
    def __init__(self, i2c, address=0x40):
        self.i2c = i2c
        self.address = address
        self._write(0x00, 0x00)  # Mode1
        self.set_pwm_freq(30)  # Establece la frecuencia por defecto a 30 Hz

    def _write(self, reg, value):
        self.i2c.writeto_mem(self.address, reg, bytes([value & 0xFF]))

    def _read(self, reg):
        return self.i2c.readfrom_mem(self.address, reg, 1)[0]

    def set_pwm_freq(self, freq):
        prescale_val = int(25000000.0 / (4096 * freq) - 1)
        old_mode = self._read(0x00)
        new_mode = (old_mode & 0x7F) | 0x10  # sleep
        self._write(0x00, new_mode)
        self._write(0xFE, prescale_val)
        self._write(0x00, old_mode)
        time.sleep(0.005)
        self._write(0x00, old_mode | 0x80)  # wake up

    def set_pwm(self, channel, on, off):
        self._write(0x06 + 4 * channel, on & 0xFF)
        self._write(0x07 + 4 * channel, (on >> 8) & 0xFF)
        self._write(0x08 + 4 * channel, off & 0xFF)
        self._write(0x09 + 4 * channel, (off >> 8) & 0xFF)

    def set_servo_angle(self, channel, angle):
        duty_cycle = int((angle / 180.0) * 4095)
        self.set_pwm(channel, 0, duty_cycle)
