# test_hcsr04.py
# Standalone test for HC-SR04 distance sensor.
# Run via REPL:  import test_hcsr04
# Stop with:    Ctrl+C

import time
from lib.sensor_hcsr04 import read_cm, TRIG_PIN, ECHO_PIN


def test():
    print('================================')
    print('  HC-SR04 Distance Sensor Test')
    print('================================')
    print(' TRIG pin : GPIO %d' % TRIG_PIN)
    print(' ECHO pin : GPIO %d' % ECHO_PIN)
    print()
    print(' Reading distance every 1 second.')
    print(' Press Ctrl+C to stop.')
    print()

    count = 0

    try:
        while True:
            d = read_cm()

            count += 1
            if d is None:
                print(' [%d] OUT OF RANGE / TIMEOUT' % count)
            else:
                print(' [%d] Distance: %.1f cm' % (count, d))

            time.sleep(1)

    except KeyboardInterrupt:
        print()
        print('Test stopped by user.')
        print('%d readings taken.' % count)


# Run on import (MicroPython friendly).
test()
