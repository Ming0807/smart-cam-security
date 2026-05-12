# test_full_local_alert_sd.py
# Full detection pipeline:
#   sensor -> trigger -> Telegram text -> capture -> save SD -> Telegram photo
#
# Run via REPL:  import test_full_local_alert_sd
# Stop with:    Ctrl+C
#
# No flash LED (GPIO4/SD conflict).  Requires config.py with Wi-Fi + Telegram.

import time
import gc

from lib.logger import info, warn, error
from lib.wifi_manager import connect as wifi_connect
from lib.sd_storage import mount_sd, list_files
from lib.sensor_hcsr04 import read_cm
from lib.trigger_controller import TriggerController
# Camera + full_alert_workflow imports delayed — SD must mount first.


def _load_config():
    try:
        import config
        return config
    except ImportError:
        return None


def test():
    info('=====================================')
    info('  Full Alert Pipeline  (no flash)')
    info('=====================================')
    info('Threshold : 50 cm')
    info('Cooldown  : 15 seconds')
    info('Flash     : OFF')
    info('Output    : Telegram + SD')
    info('')

    # ---- Config ----
    cfg = _load_config()
    if cfg is None:
        error('config.py not found.')
        return

    # ---- Wi-Fi ----
    if not cfg.WIFI_SSID or cfg.WIFI_SSID == 'YOUR_SSID':
        error('Wi-Fi not configured.')
        return

    info('Step 1: Wi-Fi...')
    wlan = wifi_connect(cfg.WIFI_SSID, cfg.WIFI_PASSWORD)
    if wlan is None:
        error('Wi-Fi failed.')
        return
    info('PASS: Wi-Fi')

    # ---- Telegram config ----
    token = getattr(cfg, 'TELEGRAM_BOT_TOKEN', '')
    chat_id = getattr(cfg, 'TELEGRAM_CHAT_ID', '')
    device = getattr(cfg, 'DEVICE_ID', 'esp32cam-01')
    if not token or not chat_id:
        error('Telegram not configured in config.py')
        return
    info('Telegram: OK (%s)' % device)

    # ---- SD (before camera!) ----
    info('Step 2: Mount SD...')
    if not mount_sd():
        error('SD mount failed.')
        return
    info('PASS: SD mounted')

    # ---- Camera (after SD!) ----
    from lib.camera_manager import init as cam_init
    from lib.camera_manager import deinit as cam_deinit

    info('Step 3: Camera...')
    if not cam_init(framesize=5):
        error('Camera init failed.')
        return
    info('PASS: Camera ready')

    # Import full alert workflow after camera init.
    from lib.full_alert_workflow import run_detection_alert_cycle

    # ---- Trigger ----
    tc = TriggerController(distance_cm=50, cooldown_sec=15)
    info('Step 4: Sensor ready')
    info('')

    info('Reading every 1s.  Press Ctrl+C to stop.')
    info('')

    capture_count = 0
    read_count = 0

    try:
        while True:

            read_count += 1
            d = read_cm()

            if d is None:
                print(' [%d] --- out of range' % read_count)
            else:
                cd = tc.cooldown_remaining_sec()
                if cd > 0:
                    print(' [%d] %.1f cm  (cooldown %ds)' % (read_count, d, int(cd)))
                else:
                    print(' [%d] %.1f cm  (armed)' % (read_count, d))

            if tc.should_trigger(d):
                capture_count += 1
                info('')
                info('=== DETECTION #%d (%.1f cm) ===' % (capture_count, d))

                cycle = run_detection_alert_cycle(token, chat_id, device, d)

                info('--- Result ---')
                info('  Text:    %s' % ('OK' if cycle['text_sent'] else 'FAIL'))
                info('  Capture: %s (%d bytes)' % (
                    'OK' if cycle['image_captured'] else 'FAIL',
                    cycle['image_size']))
                info('  SD save: %s' % ('OK' if cycle['saved_to_sd'] else 'FAIL'))
                info('  Photo:   %s' % ('OK' if cycle['photo_sent'] else 'FAIL'))
                if cycle['path']:
                    info('  File:    %s' % cycle['path'])

                info('Cooldown %ds. Free mem: %d' % (
                    tc.cooldown_ms // 1000, gc.mem_free()))
                info('')

            time.sleep(1)

    except KeyboardInterrupt:
        info('')
        info('Stopped. %d readings, %d detections.' % (read_count, capture_count))

    cam_deinit()
    info('Camera released. Done.')


test()
