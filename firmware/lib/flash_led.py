# lib/flash_led.py
# Built-in flash LED control for ESP32-CAM.
#
# The ESP32-CAM has a white LED on GPIO4.
#
# WARNING: GPIO4 is shared with the MicroSD card in 4-bit mode.
#   If you use SD card in 4-bit mode, DO NOT use the flash LED
#   at the same time — it will cause SD read/write errors.
#   Use 1-bit SD mode instead, or disable flash when SD is active.
#
# Default state is OFF (safe for SD card).

import machine
import time

# ---------- config ----------
FLASH_PIN = 4

# ---------- pin ----------
_led = machine.Pin(FLASH_PIN, machine.Pin.OUT)
_led.value(0)  # start OFF


def init_flash():
    """ Ensure pin is configured as output and OFF. """
    _led.value(0)


def flash_on():
    """ Turn flash LED ON. """
    _led.value(1)


def flash_off():
    """ Turn flash LED OFF. """
    _led.value(0)


def flash_pulse(duration_ms=200):
    """
    Turn flash ON for `duration_ms`, then OFF.
    Blocks for the pulse duration.
    """
    _led.value(1)
    time.sleep_ms(duration_ms)
    _led.value(0)
