# lib/full_alert_workflow.py
# Full detection alert cycle:
#   Telegram text -> camera capture -> save SD -> Telegram photo
#
# Each step is independent — failure in one does not block the next.

import gc
from lib.logger import info, warn, error
from lib.alert_workflow import send_detection_text_alert
from lib.local_event_storage import save_motion_image_to_sd
from lib.telegram_client import send_photo_message
# Camera import delayed — ISR blocks SD mount.
# Imported inside run_detection_alert_cycle() after SD is ready.


def run_detection_alert_cycle(token, chat_id, device_id, distance_cm):
    """
    Run the full detection cycle once.

    Returns dict:
        { 'success': bool,
          'text_sent': bool,
          'image_captured': bool,
          'saved_to_sd': bool,
          'photo_sent': bool,
          'filename': str,
          'path': str,
          'image_size': int,
          'error': str or None }
    """

    result = {
        'success': False,
        'text_sent': False,
        'image_captured': False,
        'saved_to_sd': False,
        'photo_sent': False,
        'filename': '',
        'path': '',
        'image_size': 0,
        'error': None,
    }

    # ---- 1. Telegram text alert ----
    gc.collect()
    alert = send_detection_text_alert(token, chat_id, device_id, distance_cm)
    result['text_sent'] = alert['success']
    if not alert['success']:
        warn('Telegram text failed: %s' % alert['message'])
    else:
        info('Telegram text: OK')

    # ---- 2. Camera capture ----
    from lib.camera_manager import capture as cam_capture
    from lib.camera_manager import deinit as cam_deinit
    from lib.camera_manager import init as cam_init

    info('Capturing...')
    jpeg = cam_capture()
    if jpeg is None or len(jpeg) == 0:
        result['error'] = 'Camera capture failed'
        return result

    result['image_captured'] = True
    result['image_size'] = len(jpeg)
    info('Captured: %d bytes' % len(jpeg))

    # ---- 3. Save to SD ----
    sd_result = save_motion_image_to_sd(jpeg, distance_cm=distance_cm)
    result['saved_to_sd'] = sd_result['success']
    result['filename'] = sd_result['filename']
    result['path'] = sd_result['path']
    if not sd_result['success']:
        warn('SD save failed: %s' % sd_result['error'])
    else:
        info('Saved: %s' % sd_result['path'])

    # ---- 4. Telegram photo (deinit camera to free RAM) ----
    caption = 'Distance: %.1f cm' % distance_cm
    if result['filename']:
        caption += ' | %s' % result['filename']

    cam_deinit()
    gc.collect()
    info('Camera released. Free mem: %d' % gc.mem_free())

    info('Sending photo to Telegram...')
    photo = send_photo_message(token, chat_id, jpeg, caption=caption)
    result['photo_sent'] = photo['success']
    if not photo['success']:
        warn('Telegram photo failed: %s' % photo['message'])
    else:
        info('Telegram photo: OK')

    # Re-init camera for next cycle.
    cam_init(framesize=5)
    gc.collect()

    # Overall success: at least image was saved somewhere.
    result['success'] = result['image_captured'] and (
        result['saved_to_sd'] or result['photo_sent']
    )

    gc.collect()
    return result
