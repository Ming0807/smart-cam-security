# test_flash_led.py
# Standalone test for ESP32-CAM built-in flash LED (GPIO4).
#
# Run via REPL:  import test_flash_led
# Stop with:    Ctrl+C
#
# WARNING: GPIO4 conflicts with MicroSD in 4-bit mode.
#   Remove SD card or use 1-bit mode when using flash LED.

import time
from lib.flash_led import init_flash, flash_on, flash_off, flash_pulse, FLASH_PIN


def test():
    print('================================')
    print('  Flash LED Test (GPIO %d)' % FLASH_PIN)
    print('================================')
    print()

    init_flash()
    print('Flash pin ready. GPIO%d = OUTPUT, OFF.' % FLASH_PIN)
    print()

    try:
        for i in range(1, 4):
            print('Pulse %d/3: ON ...' % i)
            flash_pulse(200)
            print('Pulse %d/3: OFF' % i)
            time.sleep(1)

        print()
        print('All pulses complete. Flash is OFF.')
        print('If you saw 3 brief flashes, GPIO4 works.')

    except KeyboardInterrupt:
        flash_off()
        print()
        print('Test stopped. Flash turned OFF.')

    flash_off()


test()
