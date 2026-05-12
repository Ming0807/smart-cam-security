# Skill: Telegram Bot

## Use This Skill When

Working on Telegram alerts or inline buttons.

## MVP Flow

1. Send text alert.
2. Send snapshot photo.
3. Include timestamp, distance, and device ID.

## Rules

- Do not commit bot token.
- Send text before photo.
- Use retries with maximum attempts.
- Do not upload videos in MVP.
- Add inline buttons after base alert is stable.

## Inline Button Flow

Telegram button should create a cloud command, not directly connect to ESP32-CAM.
