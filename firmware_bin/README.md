# Firmware Binary

## Source

LeMaRiva MicroPython Camera Driver for ESP32-CAM
https://github.com/lemariva/micropython-camera-driver

## File

`micropython_camera_feeeb5ea3_esp32_idf4_4.bin`

## How to Download

Download the precompiled `.bin` from the LeMaRiva repository:

1. Go to https://github.com/lemariva/micropython-camera-driver
2. Navigate to the `firmware/` directory.
3. Download `micropython_camera_feeeb5ea3_esp32_idf4_4.bin`.
4. Place it in this folder (`firmware_bin/`).

Do not rename the file. The flashing script expects the exact filename.

## Notes

- This firmware includes the `camera` module for OV2640 on AI-Thinker ESP32-CAM.
- Flash address is `0x1000`.
- The `.bin` file is excluded from Git via `.gitignore`.
- Do not compile from source — use the precompiled binary.
