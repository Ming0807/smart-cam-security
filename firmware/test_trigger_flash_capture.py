# test_trigger_flash_capture.py
# Integrated test: sensor -> trigger -> flash -> capture -> save.
#
# Run via REPL:  import test_trigger_flash_capture
# Stop with:    Ctrl+C   (flash always turns OFF)

import time
import gc

from lib.logger import info, warn, error
from lib.camera_manager import init as cam_init
from lib.camera_manager import deinit as cam_deinit
from lib.sensor_hcsr04 import read_cm
from lib.trigger_controller import TriggerController
from lib.flash_led import init_flash, flash_off
from lib.capture_workflow import capture_with_optional_flash


def test():
    info('================================')
    info('  Trigger + Flash + Capture Test')
    info('================================')
    info('Threshold : 50 cm')
    info('Cooldown  : 15 seconds')
    info('Flash     : ON  (GPIO4, 200ms warmup)')
    info('')

    # --- Camera ---
    info('Initializing camera...')
    if not cam_init(framesize=5):
        error('Camera init failed — abort.')
        return
    info('Camera ready')

    # --- Flash ---
    init_flash()
    info('Flash LED ready (GPIO4, OFF)')

    # --- Trigger ---
    tc = TriggerController(distance_cm=50, cooldown_sec=15)
    info('Trigger controller ready')
    info('')

    info('Reading sensor every 1s.  Press Ctrl+C to stop.')
    info('')

    capture_count = 0
    read_count = 0

    try:
        while True:

            read_count += 1
            d = read_cm()

            # --- Print status ---
            if d is None:
                print(' [%d] distance: --- out of range' % read_count)
            else:
                cd = tc.cooldown_remaining_sec()
                if cd > 0:
                    print(' [%d] distance: %.1f cm  (cooldown %ds)' % (read_count, d, int(cd)))
                else:
                    print(' [%d] distance: %.1f cm  (armed)' % (read_count, d))

            # --- Trigger ---
            if tc.should_trigger(d):
                capture_count += 1
                info('')
                info('TRIGGER! Object at %.1f cm' % d)

                # Use the integrated workflow: flash + capture + save.
                name = 'motion_flash_%03d.jpg' % capture_count
                info('Flash ON  ->  capturing...')
                result = capture_with_optional_flash(
                    flash_enabled=True,
                    flash_warmup_ms=200,
                    filename=name,
                )

                # Result handling.
                if result['success']:
                    info('Flash OFF.  Saved: %s (%d bytes)' % (
                        result['filename'], result['size']))
                else:
                    error('Failed: %s' % result['error'])

                info('Cooldown %ds started.' % (tc.cooldown_ms // 1000))
                gc.collect()
                info('Free mem: %d bytes' % gc.mem_free())
                info('')

            time.sleep(1)

    except KeyboardInterrupt:
        info('')
        info('Test stopped by user.')
        info('%d readings, %d captures.' % (read_count, capture_count))

    # --- Cleanup ---
    flash_off()
    cam_deinit()
    info('Flash OFF. Camera released.')
    info('Done.')


test()
