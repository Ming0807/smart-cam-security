# test_sd_card.py
# Standalone MicroSD card test:
#   Mount -> write test file -> read back -> list files.
#
# Run via REPL:  import test_sd_card
#
# No camera, no sensor, no Telegram, no flash — SD only.

from lib.logger import info, warn, error
from lib.sd_storage import (
    mount_sd, is_mounted,
    write_text_file, read_text_file,
    list_files, get_free_space,
)


def test():
    print('================================')
    print('  MicroSD Card Test')
    print('================================')
    print()

    # 1. Mount.
    print('--- 1. Mount SD card ---')
    ok = mount_sd()
    if not ok:
        error('SD mount failed. Aborting test.')
        error('')
        error('Troubleshooting:')
        error('  - Is MicroSD inserted?')
        error('  - Formatted as FAT32?')
        error('  - Reliable brand (not fake)?')
        error('  - Try power-cycling the board.')
        return

    print('PASS: SD mounted — seeing files...')
    print()

    # 2. List existing files.
    print('--- 2. List files on SD ---')
    files = list_files()
    if files:
        for f in files:
            print('  %s' % f)
    else:
        print('  (empty)')
    print()

    # 3. Check free space.
    free = get_free_space()
    if free > 0:
        free_mb = free / (1024 * 1024)
        print('Free space: %.1f MB' % free_mb)
    print()

    # 4. Write test file.
    print('--- 3. Write test file ---')
    ok = write_text_file('test_sd.txt', 'Hello from ESP32-CAM MicroPython!\nSD card works.\n')
    if not ok:
        return
    print('PASS: File written')

    # 5. Read test file back.
    print('--- 4. Read test file ---')
    content = read_text_file('test_sd.txt')
    if content is None:
        return
    print('File content:')
    print('  ' + content.replace('\n', '\n  ').rstrip())
    print()
    print('PASS: File read back')

    # 6. List again.
    print('--- 5. Final file list ---')
    files = list_files()
    for f in files:
        print('  %s' % f)

    print()
    info('SD card test complete — all passed.')
    print()
    print('Next: save JPEG photos to SD.')


test()
