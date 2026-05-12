# lib/capture_workflow.py
# Integrated capture workflow: flash LED + camera capture + save.
#
# GPIO4 flash LED conflicts with MicroSD 4-bit mode.
# Keep flash_enabled configurable so it can be disabled when SD is active.

import gc
from lib.logger import info, warn, error
from lib.flash_led import flash_on, flash_off
from lib.camera_manager import capture as cam_capture
from lib.camera_manager import save as cam_save


def capture_with_optional_flash(flash_enabled=True, flash_warmup_ms=200, filename=None):
    """
    Run one capture cycle, optionally with flash LED.

    Returns a dict:
      { 'success': True/False,
        'filename': str or None,
        'size': int (image bytes) or 0,
        'error': str or None }
    """

    result = {
        'success': False,
        'filename': filename,
        'size': 0,
        'error': None,
    }

    jpeg = None

    try:
        # -- Flash ON --
        if flash_enabled:
            flash_on()

        # -- Wait for flash to stabilise --
        if flash_enabled and flash_warmup_ms > 0:
            import time
            time.sleep_ms(flash_warmup_ms)

        # -- Capture --
        gc.collect()
        jpeg = cam_capture()
        if jpeg is None or len(jpeg) == 0:
            result['error'] = 'Camera capture returned no data'
            return result

        result['size'] = len(jpeg)

        # -- Save --
        if filename is not None:
            if not cam_save(jpeg, filename):
                result['error'] = 'Failed to save %s' % filename
                return result
        else:
            # Even without save, success is True if we got a valid image.
            pass

        result['success'] = True
        info('Capture workflow OK (%d bytes)' % result['size'])
        return result

    except Exception as e:
        error('Capture workflow error: %s' % e)
        result['error'] = str(e)
        return result

    finally:
        # -- Flash OFF -- always, even on error.
        if flash_enabled:
            flash_off()
