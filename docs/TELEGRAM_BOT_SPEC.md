# Telegram Bot Specification

## Purpose

Telegram is used for fast mobile alert notifications and quick actions.

## Required MVP Behavior

When detection occurs:

1. Send text alert.
2. Send JPEG snapshot.
3. Include event details.

## Message Format

Example:

```text
🚨 ตรวจพบวัตถุใกล้กล้อง

Device: esp32cam-01
Time: 2026-05-12 18:30:22
Distance: 43 cm
File: motion_20260512_183022.jpg
Status: Armed
```

## Photo Caption

```text
Distance: 43 cm | motion_sd_20260513_021500.jpg
```

## Implementation

- Text: `telegram_client.send_text_message()` via raw socket+SSL GET
- Photo: `telegram_client.send_photo_message()` via multipart/form-data POST
- Full cycle: `full_alert_workflow.run_detection_alert_cycle()`

## Inline Buttons

Add after MVP alert works.

Recommended buttons:

- Open Dashboard
- Disarm
- Mute
- Delete Latest File

## Callback Flow

```text
User clicks Telegram button
  ↓
Telegram sends callback to Next.js API
  ↓
Next.js validates callback
  ↓
Next.js creates device command in Supabase
  ↓
ESP32-CAM polls command
  ↓
ESP32-CAM executes command
```

## Security

- Do not commit `TELEGRAM_BOT_TOKEN`.
- Do not expose token in client code.
- Use environment variables in Next.js.
- Use local secret config file on ESP32-CAM and ignore it in Git.

## MVP Rule

Do not send video files in MVP.

Reason:

- Large payloads increase failure rate.
- ESP32-CAM memory is limited.
- Uploading video may delay alert.
