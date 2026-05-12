# lib/media_storage.py
# Save captured JPEG images to MicroSD card.
# Filenames use a simple counter or ticks-based naming.

import time
from lib.logger import info, warn, error
from lib.sd_storage import is_mounted, write_binary

# Counter for sequential filenames (resets on import).
_file_counter = 0


def save_jpeg_to_sd(image_bytes, filename=None, folder=''):
    """
    Save JPEG bytes to MicroSD card.

    If `filename` is None, auto-generates 'cap_001.jpg', 'cap_002.jpg', ...
    If `folder` is set, saves into /sd/<folder>/filename.

    Returns dict:
        { 'success': bool,
          'filename': str,
          'path': str (full /sd/... path),
          'size': int (bytes written),
          'error': str or None }
    """

    result = {
        'success': False,
        'filename': '',
        'path': '',
        'size': 0,
        'error': None,
    }

    if not is_mounted():
        result['error'] = 'SD card not mounted'
        return result

    if not image_bytes:
        result['error'] = 'No image data received'
        return result

    # Build filename.
    global _file_counter
    if filename is None:
        _file_counter += 1
        filename = 'cap_%03d.jpg' % _file_counter

    # Build path.
    if folder:
        path = '%s/%s' % (folder, filename)
    else:
        path = filename

    result['filename'] = filename
    result['path'] = '/sd/' + path
    result['size'] = len(image_bytes)

    if not write_binary(path, image_bytes):
        result['error'] = 'Write to SD failed'
        return result

    result['success'] = True
    info('Saved to SD: %s (%d bytes)' % (result['path'], result['size']))
    return result


def make_timestamp_filename(prefix='cap', ext='.jpg'):
    """
    Generate a filename with a simple timestamp.
    Example: cap_20260513_013000.jpg
    """
    t = time.localtime()
    ts = '%04d%02d%02d_%02d%02d%02d' % (
        t[0], t[1], t[2], t[3], t[4], t[5]
    )
    return '%s_%s%s' % (prefix, ts, ext)
