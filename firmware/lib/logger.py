# lib/logger.py
# Simple timestamped console logging.

import time


def _now():
    t = time.localtime()
    return '%04d-%02d-%02d %02d:%02d:%02d' % (
        t[0], t[1], t[2], t[3], t[4], t[5]
    )


def info(msg):
    print('[%s] %s' % (_now(), msg))


def warn(msg):
    print('[%s] WARN  %s' % (_now(), msg))


def error(msg):
    print('[%s] ERROR %s' % (_now(), msg))
