# lib/telegram_client.py
# Telegram Bot API client for MicroPython using raw sockets + SSL.
# Does NOT require urequests — works with built-in socket/ssl only.

import socket
import ssl
import gc
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
    gc.collect()
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


def send_photo_message(token, chat_id, image_bytes, caption=None):
    """
    Send a JPEG photo via Telegram Bot API (multipart/form-data POST).
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

    if not image_bytes:
        result['message'] = 'No image data'
        return result

    host = 'api.telegram.org'
    path = '/bot%s/sendPhoto' % token

    # Build multipart body.
    boundary = '----ESP32CAM'
    eol = '\r\n'

    body = b''
    body += ('--%s' % boundary + eol).encode()
    body += ('Content-Disposition: form-data; name="chat_id"' + eol + eol).encode()
    body += (str(chat_id) + eol).encode()

    body += ('--%s' % boundary + eol).encode()
    body += ('Content-Disposition: form-data; name="photo"; filename="capture.jpg"' + eol).encode()
    body += ('Content-Type: image/jpeg' + eol + eol).encode()
    body += image_bytes
    body += (eol).encode()

    if caption:
        body += ('--%s' % boundary + eol).encode()
        body += ('Content-Disposition: form-data; name="caption"' + eol + eol).encode()
        body += (caption + eol).encode()

    body += ('--%s--' % boundary + eol).encode()

    content_length = len(body)

    info('Telegram: sending photo (%d bytes)...' % content_length)

    gc.collect()
    addr = socket.getaddrinfo(host, 443)[0][-1]
    s = socket.socket()
    s.settimeout(30)

    try:
        s.connect(addr)
        s = ssl.wrap_socket(s)

        header = (
            'POST %s HTTP/1.1\r\n'
            'Host: %s\r\n'
            'Content-Type: multipart/form-data; boundary=%s\r\n'
            'Content-Length: %d\r\n'
            'Connection: close\r\n'
            '\r\n'
        ) % (path, host, boundary, content_length)
        s.write(header.encode())
        s.write(body)

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

        text = buf.decode('utf-8', 'ignore')

        status_code = 0
        try:
            status_line = text.split('\r\n')[0]
            status_code = int(status_line.split(' ')[1])
        except:
            pass

        result['status_code'] = status_code

        if status_code == 200 and ('"ok":true' in text or '"ok": true' in text):
            result['success'] = True
            result['message'] = 'Photo sent OK'
        else:
            body_text = ''
            if '\r\n\r\n' in text:
                body_text = text.split('\r\n\r\n', 1)[1][:120]
            result['message'] = 'HTTP %d: %s' % (status_code, body_text)

    except Exception as e:
        result['message'] = 'Network error: %s' % e

    finally:
        try:
            s.close()
        except:
            pass

    return result
