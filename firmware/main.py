# main.py
# Phase 1: Firmware Bring-Up
# Wi-Fi + Camera validation for ESP32-CAM (LeMaRiva firmware).

import gc
import sys

from lib.logger import info, warn, error
from lib.wifi_manager import connect
from lib.camera_manager import camera_ok as cam_ok
from lib.camera_manager import init as cam_init
from lib.camera_manager import capture as cam_capture
from lib.camera_manager import save as cam_save
from lib.camera_manager import deinit as cam_deinit


def _load_config():
    try:
        import config
        return config
    except ImportError:
        return None


def run():
    info('')
    info('=== Phase 1: Firmware Bring-Up ===')
    info('uPython: %s' % sys.version.split(';')[0].strip())
    gc.collect()
    info('Free mem: %d bytes' % gc.mem_free())

    # -- Config --
    cfg = _load_config()
    if cfg is None:
        warn('config.py not found. Wi-Fi will be skipped.')
        info('Copy config.example.py to config.py and fill credentials.')
        wlan = None
    else:
        wlan = connect(cfg.WIFI_SSID, cfg.WIFI_PASSWORD)

    if wlan is not None:
        info('PASS: Wi-Fi connected')
    else:
        warn('SKIP: Wi-Fi not connected (no config or failed)')

    # -- Camera --
    if not cam_ok:
        error('FAIL: Camera module not available')
        error('Flash LeMaRiva firmware before running this test.')
        return

    if not cam_init(framesize=0):
        error('FAIL: Camera init')
        return
    info('PASS: Camera init')

    jpeg = cam_capture()
    if jpeg is None:
        cam_deinit()
        error('FAIL: JPEG capture')
        return
    info('PASS: JPEG captured')

    if not cam_save(jpeg):
        cam_deinit()
        error('FAIL: Save test.jpg')
        return
    info('PASS: test.jpg saved')

    cam_deinit()
    gc.collect()
    info('Free mem: %d bytes' % gc.mem_free())

    info('')
    info('=== Phase 1 Complete ===')
    info('Camera:  PASS')
    info('Output:  test.jpg')
    info('')
    info('Next: Phase 2 — Sensor + SD Card')


# Run on import (MicroPython auto-runs main.py on boot)
run()
