# Skill: MicroPython ESP32-CAM

## Use This Skill When

Working on ESP32-CAM firmware.

## Core Rules

- Firmware must be MicroPython.
- Use camera-enabled MicroPython build.
- Start with JPEG snapshot.
- Avoid AVI in MVP.
- Keep memory usage low.
- Use network timeouts.
- Avoid blocking forever.
- Respect pin mapping.

## Typical Tasks

- Connect to Wi-Fi
- Initialize camera
- Capture JPEG
- Save JPEG to SD
- Read HC-SR04 distance
- Send Telegram alert
- POST event log
- Poll cloud commands

## Avoid

- Arduino C++ code
- ESP-IDF code
- Heavy video processing
- Long-running blocking loops
