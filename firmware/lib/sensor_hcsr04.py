# lib/sensor_hcsr04.py
# HC-SR04 ultrasonic distance sensor driver for ESP32-CAM MicroPython.
#
# Wiring:
#   TRIG -> GPIO 12 (output)
#   ECHO -> GPIO 13 (input, MUST use voltage divider: 5V -> 3.3V)
#   VCC  -> 5V pin
#   GND  -> GND
#
# Voltage divider (required!):
#   ECHO ----[1kΩ]----+---- GPIO 13
#                      |
#                    [2kΩ]
#                      |
#                     GND

import machine
import time

# ---------- config ----------
TRIG_PIN = 12
ECHO_PIN = 13

# Sound travels at ~343 m/s = 0.0343 cm per microsecond.
# Round-trip divided by 2 gives one-way distance.
SPEED_OF_SOUND_CM_PER_US = 0.0343

# Maximum measurable distance: ~500 cm in ~30,000 us.
ECHO_TIMEOUT_US = 30000

# Maximum valid distance in cm. Ignore anything beyond this.
MAX_DISTANCE_CM = 400

# ---------- pins ----------
trig = machine.Pin(TRIG_PIN, machine.Pin.OUT)
echo = machine.Pin(ECHO_PIN, machine.Pin.IN)

# Ensure trigger starts LOW.
trig.value(0)


def read_cm():
    """
    Send a 10us trigger pulse and measure the echo pulse width.
    Returns distance in centimetres, or None on timeout / bad reading.
    """

    # 1. Send trigger pulse.
    trig.value(0)
    time.sleep_us(2)
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)

    # 2. Measure ECHO pin HIGH time.
    #    time_pulse_us(pin, level, timeout) blocks until the pin
    #    reads `level` (1), then returns the pulse length in µs.
    #    Returns -1 on timeout.
    duration_us = machine.time_pulse_us(echo, 1, ECHO_TIMEOUT_US)

    # 3. Timeout — no object in range (or wiring issue).
    if duration_us < 0:
        return None

    # 4. Convert to centimetres.
    distance_cm = duration_us * SPEED_OF_SOUND_CM_PER_US / 2.0

    # 5. Reject readings that are clearly invalid.
    if distance_cm <= 0 or distance_cm > MAX_DISTANCE_CM:
        return None

    return round(distance_cm, 1)


def cleanup():
    """ Release pins (optional — MicroPython handles this on reset). """
    trig.value(0)
