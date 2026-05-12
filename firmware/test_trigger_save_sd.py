# test_trigger_save_sd.py
# Sensor -> trigger -> camera -> save JPEG to MicroSD.
#
# Run via REPL:  import test_trigger_save_sd
# Stop with:    Ctrl+C
#
# No Wi-Fi, no flash, no Telegram — sensor + camera + SD only.

import time
import gc

from lib.logger import info, warn, error
from lib.sd_storage import mount_sd, list_files
from lib.sensor_hcsr04 import read_cm
from lib.trigger_controller import TriggerController
from lib.local_event_storage import save_motion_image_to_sd

# Delay camera imports — camera ISR blocks SD mount.
# Imported inside test() after SD is mounted.


def test():
    info('================================')
    info('  Trigger -> Camera -> Save SD')
    info('================================')
    info('Threshold : 50 cm')
    info('Cooldown  : 15 seconds')
    info('Flash     : OFF (safe for SD)')
    info('Save to   : /sd/')
    info('')

    # ---- 1. Mount SD (must be before camera) ----
    info('Step 1: Mount SD (slot=1, width=1)...')
    if not mount_sd():
        error('SD mount failed.')
        return
    info('PASS: SD mounted')

    # ---- 2. Init camera (import after SD!) ----
    from lib.camera_manager import init as cam_init
    from lib.camera_manager import capture as cam_capture
    from lib.camera_manager import deinit as cam_deinit

    info('Step 2: Initialize camera...')
    if not cam_init(framesize=5):
        error('Camera init failed.')
        return
    info('PASS: Camera ready')

    # ---- 3. Trigger ----
    tc = TriggerController(distance_cm=50, cooldown_sec=15)
    info('Step 3: Trigger ready')
    info('')

    info('Reading sensor every 1s.  Press Ctrl+C to stop.')
    info('')

    capture_count = 0
    read_count = 0

    try:
        while True:

            read_count += 1
            d = read_cm()

            # ---- Status ----
            if d is None:
                print(' [%d] --- out of range' % read_count)
            else:
                cd = tc.cooldown_remaining_sec()
                if cd > 0:
                    print(' [%d] %.1f cm  (cooldown %ds)' % (read_count, d, int(cd)))
                else:
                    print(' [%d] %.1f cm  (armed)' % (read_count, d))

            # ---- Trigger ----
            if tc.should_trigger(d):
                capture_count += 1
                info('')
                info('=== DETECTION #%d ===' % capture_count)
                info('Distance: %.1f cm' % d)

                # Capture.
                info('Capturing...')
                jpeg = cam_capture()
                if jpeg is None:
                    error('Capture failed — no image data')
                    info('Cooldown %ds. Waiting...' % (tc.cooldown_ms // 1000))
                    info('')
                    time.sleep(1)
                    continue

                info('Captured: %d bytes' % len(jpeg))

                # Save to SD.
                result = save_motion_image_to_sd(jpeg, distance_cm=d)
                if result['success']:
                    info('Saved: %s' % result['path'])

                    # Quick file listing.
                    files = list_files()
                    jpg_count = sum(1 for f in files if f.endswith('.jpg'))
                    info('  SD: %d files (%d JPEGs)' % (len(files), jpg_count))
                else:
                    error('Save failed: %s' % result['error'])

                gc.collect()
                info('Cooldown %ds. Free mem: %d bytes' % (
                    tc.cooldown_ms // 1000, gc.mem_free()))
                info('')

            time.sleep(1)

    except KeyboardInterrupt:
        info('')
        info('Stopped. %d readings, %d captures.' % (read_count, capture_count))

    cam_deinit()
    info('Camera released.')
    info('Done.')


test()
