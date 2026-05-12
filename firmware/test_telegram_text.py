# test_telegram_text.py
# Standalone test: Wi-Fi + Telegram text message.
#
# Run via REPL:  import test_telegram_text
#
# Requires config.py with real TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID.

from lib.logger import info, warn, error
from lib.wifi_manager import connect as wifi_connect
from lib.telegram_client import send_text_message


def _load_config():
    try:
        import config
        return config
    except ImportError:
        return None


def test():
    info('================================')
    info('  Telegram Text Message Test')
    info('================================')
    info('')

    # -- Load config --
    cfg = _load_config()
    if cfg is None:
        error('config.py not found.')
        error('Copy config.example.py to config.py and fill values.')
        return

    # -- Wi-Fi --
    if not cfg.WIFI_SSID or cfg.WIFI_SSID == 'YOUR_SSID':
        error('Wi-Fi credentials not set in config.py')
        return

    wlan = wifi_connect(cfg.WIFI_SSID, cfg.WIFI_PASSWORD)
    if wlan is None:
        error('Wi-Fi connection failed.')
        return
    info('PASS: Wi-Fi connected')

    # -- Validate Telegram config --
    token = getattr(cfg, 'TELEGRAM_BOT_TOKEN', '')
    chat_id = getattr(cfg, 'TELEGRAM_CHAT_ID', '')

    if not token:
        error('TELEGRAM_BOT_TOKEN is empty in config.py')
        error('Create a bot with @BotFather and copy the token.')
        return

    if not chat_id:
        error('TELEGRAM_CHAT_ID is empty in config.py')
        error('Visit https://api.telegram.org/bot<TOKEN>/getUpdates to find it.')
        return

    info('')

    # -- Send test message --
    device = getattr(cfg, 'DEVICE_ID', 'esp32cam-01')
    msg = 'ESP32-CAM Telegram test from %s' % device

    info('Sending: "%s"' % msg)
    result = send_text_message(token, chat_id, msg)

    info('')
    if result['success']:
        info('PASS: Telegram message sent!')
    else:
        error('FAIL: %s' % result['message'])
        info('Status code: %d' % result['status_code'])

    info('Done.')


test()
