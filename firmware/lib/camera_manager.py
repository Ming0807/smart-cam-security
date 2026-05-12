# lib/camera_manager.py
# Camera control for ESP32-CAM using LeMaRiva firmware v1.18 i2s driver.
# camera.init() takes exactly 1 positional arg: framesize constant.
# Power cycle the board if init fails after repeated attempts.

import gc
from lib.logger import info, warn, error

# LeMaRiva i2s driver frame sizes:
#   0 = 96x96       5 = QVGA (320x240)
#   1 = QQVGA       8 = VGA  (640x480)
#   2 = QCIF       10 = SVGA
#   3 = HQVGA      ...etc

camera_ok = False

try:
    import camera
    camera_ok = True
    info('Camera module loaded')
except ImportError:
    camera = None
    error('Camera module missing!')
    error('Flash LeMaRiva firmware: micropython_camera_feeeb5ea3_esp32_idf4_4.bin')


def init(framesize=5):
    """ framesize=5 is QVGA (320x240). Pass an integer constant. """
    if not camera_ok:
        return False

    try:
        camera.deinit()
    except:
        pass

    try:
        result = camera.init(framesize)
        if result:
            info('Camera ready (framesize=%d)' % framesize)
            return True
        else:
            error('Camera init returned False (framesize=%d)' % framesize)
            return False
    except Exception as e:
        error('Camera init error: %s' % e)
        error('Try power-cycling the board (unplug USB, wait, replug)')
        return False


def capture():
    if not camera_ok:
        return None
    try:
        gc.collect()
        buf = camera.capture()
        if not buf or len(buf) == 0:
            warn('Capture returned empty buffer')
            return None
        info('Captured %d bytes' % len(buf))
        return buf
    except Exception as e:
        error('Capture error: %s' % e)
        return None


def save(buf, filename='test.jpg'):
    try:
        with open(filename, 'wb') as f:
            f.write(buf)
        info('Saved: %s (%d bytes)' % (filename, len(buf)))
        return True
    except OSError as e:
        error('Save error: %s' % e)
        return False


def deinit():
    if camera_ok and camera is not None:
        try:
            camera.deinit()
            info('Camera deinitialized')
        except Exception as e:
            warn('Deinit warning: %s' % e)
