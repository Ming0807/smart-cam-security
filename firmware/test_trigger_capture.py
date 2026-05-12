# test_trigger_capture.py
# Standalone test for trigger logic:
#   Read HC-SR04 -> if distance < 50cm -> capture JPEG -> save
#
# Run via REPL:  import test_trigger_capture
# Stop with:    Ctrl+C

import time
import gc

from lib.logger import info, warn, error
from lib.camera_manager import init as cam_init
from lib.camera_manager import capture as cam_capture
from lib.camera_manager import save as cam_save
from lib.camera_manager import deinit as cam_deinit
from lib.sensor_hcsr04 import read_cm
from lib.trigger_controller import TriggerController


def test():
    info('================================')
    info('  Trigger + Capture Test')
    info('================================')
    info('Threshold : 50 cm')
    info('Cooldown  : 15 seconds')
    info('')

    # --- Camera init ---
    info('Initializing camera...')
    if not cam_init(framesize=5):
        error('Camera init failed — abort')
        return
    info('Camera ready')

    # --- Trigger ---
    tc = TriggerController(distance_cm=50, cooldown_sec=15)
    info('Trigger controller ready')
    info('')

    info('Reading sensor every 1s. Press Ctrl+C to stop.')
    info('')

    capture_count = 0
    read_count = 0

    try:
        while True:

            read_count += 1
            d = read_cm()

            # --- Print distance ---
            if d is None:
                print(' [%d] distance: --- out of range' % read_count)
            else:
                cd = tc.cooldown_remaining_sec()
                if cd > 0:
                    print(' [%d] distance: %.1f cm  (cooldown %ds remaining)' % (read_count, d, int(cd)))
                else:
                    print(' [%d] distance: %.1f cm  (armed)' % (read_count, d))

            # --- Check trigger ---
            if tc.should_trigger(d):
                capture_count += 1
                info('TRIGGER! Object detected at %.1f cm' % d)
                info('Cooldown started (%ds).' % (tc.cooldown_ms // 1000))

                # Capture JPEG.
                info('Capturing...')
                jpeg = cam_capture()
                if jpeg is None:
                    error('Capture returned no data — skipping save')
                    continue

                # Save with counter filename.
                name = 'motion_%03d.jpg' % capture_count
                if not cam_save(jpeg, name):
                    error('Failed to save %s' % name)
                else:
                    info('Saved: %s (%d bytes)' % (name, len(jpeg)))

                gc.collect()
                info('Free mem: %d bytes' % gc.mem_free())
                info('')

            time.sleep(1)

    except KeyboardInterrupt:
        info('')
        info('Test stopped.')
        info('%d readings, %d captures.' % (read_count, capture_count))

    cam_deinit()
    info('Camera released.')
    info('Done.')


test()
