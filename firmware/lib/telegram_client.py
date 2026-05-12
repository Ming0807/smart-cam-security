# lib/telegram_client.py
# Telegram Bot API client for MicroPython using raw sockets + SSL.
# Does NOT require urequests — works with built-in socket/ssl only.

import socket
import ssl
from lib.logger import info, warn, error


def _encode(text):
    """ Minimal URL encoding for Telegram text. """
    result = ''
    for ch in text:
        if ch == ' ':
            result += '%20'
        elif ch == '\n':
            result += '%0A'
        elif ('A' <= ch <= 'Z') or ('a' <= ch <= 'z') or ('0' <= ch <= '9'):
            result += ch
        elif ch in '-_.~':
            result += ch
        else:
            result += '%%%02X' % ord(ch)
    return result


def _http_get(host, path, timeout=15):
    """
    Minimal HTTPS GET request using socket + SSL.
    Returns (status_code, body_text).
    """
    addr = socket.getaddrinfo(host, 443)[0][-1]
    s = socket.socket()
    s.settimeout(timeout)

    try:
        s.connect(addr)
        s = ssl.wrap_socket(s)

        request = (
            'GET %s HTTP/1.1\r\n'
            'Host: %s\r\n'
            'Connection: close\r\n'
            '\r\n'
        ) % (path, host)
        s.write(request.encode())

        # Read response.
        buf = b''
        while True:
            try:
                chunk = s.read(1024)
                if not chunk:
                    break
                buf += chunk
            except:
                break

        # Parse.
        text = buf.decode('utf-8', 'ignore')

        # Extract status code.
        status_code = 0
        try:
            status_line = text.split('\r\n')[0]
            status_code = int(status_line.split(' ')[1])
        except:
            pass

        # Extract JSON body (after \r\n\r\n).
        body = ''
        if '\r\n\r\n' in text:
            body = text.split('\r\n\r\n', 1)[1]

        return status_code, body

    finally:
        try:
            s.close()
        except:
            pass


def send_text_message(token, chat_id, text):
    """
    Send a text message via Telegram Bot API.
    Returns dict: { 'success': bool, 'status_code': int, 'message': str }
    """
    result = {
        'success': False,
        'status_code': 0,
        'message': '',
    }

    if not token or not chat_id:
        result['message'] = 'Missing token or chat_id'
        return result

    host = 'api.telegram.org'
    path = '/bot%s/sendMessage?chat_id=%s&text=%s' % (token, chat_id, _encode(text))

    info('Telegram: sending text...')

    try:
        status_code, body = _http_get(host, path)

        result['status_code'] = status_code

        if status_code == 200:
            # Quick JSON parse — look for "ok":true
            if '"ok":true' in body or '"ok": true' in body:
                result['success'] = True
                result['message'] = 'Sent OK'
            else:
                result['message'] = 'Telegram API: %s' % body[:120]
        else:
            result['message'] = 'HTTP %d' % status_code

    except Exception as e:
        result['message'] = 'Network error: %s' % e

    return result
