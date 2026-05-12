# test_camera_save_sd.py
# Standalone test: camera capture -> save JPEG to MicroSD.
#
# Run via REPL:  import test_camera_save_sd
#
# No flash, no sensor, no Telegram — camera + SD only.

import gc
from lib.logger import info, warn, error
from lib.sd_storage import mount_sd, list_files
from lib.camera_manager import init as cam_init
from lib.camera_manager import capture as cam_capture
from lib.camera_manager import deinit as cam_deinit
from lib.media_storage import save_jpeg_to_sd, make_timestamp_filename


def test():
    info('================================')
    info('  Camera -> SD Capture Test')
    info('================================')
    info('')

    # ---- 1. Mount SD ----
    info('Step 1: Mount SD card...')
    if not mount_sd():
        error('SD mount failed. Cannot continue.')
        return
    info('PASS: SD mounted')

    # ---- 2. Init camera (no flash!) ----
    info('')
    info('Step 2: Initialize camera (no flash)...')
    if not cam_init(framesize=5):
        error('Camera init failed. Cannot continue.')
        return
    info('PASS: Camera ready')

    # ---- 3. Capture JPEG ----
    info('')
    info('Step 3: Capture JPEG...')
    jpeg = cam_capture()
    if jpeg is None:
        cam_deinit()
        error('Capture failed. Cannot continue.')
        return
    info('PASS: Captured %d bytes' % len(jpeg))

    # ---- 4. Save to SD ----
    info('')
    info('Step 4: Save to SD...')
    filename = make_timestamp_filename(prefix='cam_test')
    result = save_jpeg_to_sd(jpeg, filename=filename)
    if not result['success']:
        cam_deinit()
        error('Save failed: %s' % result['error'])
        return
    info('PASS: Saved as %s' % result['path'])

    # ---- 5. List SD files ----
    info('')
    info('Step 5: List files on SD...')
    files = list_files()
    info('Files on SD:')
    for f in files:
        print('  %s' % f)

    # ---- Cleanup ----
    cam_deinit()
    gc.collect()
    info('')
    info('=== Test complete ===')
    info('Camera released. SD still mounted.')
    info('Free mem: %d bytes' % gc.mem_free())


test()
