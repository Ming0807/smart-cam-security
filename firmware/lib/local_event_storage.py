# lib/local_event_storage.py
# Motion event storage — save triggered captures to MicroSD.
# Filename format: motion_sd_YYYYMMDD_HHMMSS.jpg

import time
from lib.logger import info, warn, error
from lib.sd_storage import is_mounted, write_binary


def create_motion_filename():
    t = time.localtime()
    ts = '%04d%02d%02d_%02d%02d%02d' % (
        t[0], t[1], t[2], t[3], t[4], t[5]
    )
    return 'motion_sd_%s.jpg' % ts


def save_motion_image_to_sd(image_bytes, distance_cm=None):
    """
    Save a motion-triggered JPEG to MicroSD with timestamp filename.

    Returns dict:
        { 'success': bool,
          'filename': str,
          'path': str,
          'size': int,
          'distance_cm': float or None,
          'error': str or None }
    """

    result = {
        'success': False,
        'filename': '',
        'path': '',
        'size': 0,
        'distance_cm': distance_cm,
        'error': None,
    }

    if not is_mounted():
        result['error'] = 'SD not mounted'
        return result

    if not image_bytes:
        result['error'] = 'No image data'
        return result

    filename = create_motion_filename()
    path = filename  # root of /sd

    result['filename'] = filename
    result['path'] = '/sd/' + filename
    result['size'] = len(image_bytes)

    if not write_binary(path, image_bytes):
        result['error'] = 'Write to SD failed'
        return result

    result['success'] = True
    info('Motion saved: %s (%d bytes)' % (result['path'], result['size']))
    return result
