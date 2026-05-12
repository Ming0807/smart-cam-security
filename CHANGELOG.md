# Changelog

## 0.3.2 - Phase 2D: Flash LED Control

### Added

- `firmware/lib/flash_led.py` — GPIO4 flash LED: `flash_on()`, `flash_off()`, `flash_pulse(ms)`, default OFF
- `firmware/test_flash_led.py` — standalone test: 3 pulses of 200ms, Ctrl+C safe cleanup

### Notes

- GPIO4 conflicts with MicroSD DAT1 in 4-bit SD mode — must use 1-bit mode or disable flash
- Updated `docs/PIN_MAPPING.md` with flash LED section and conflict warning
- Updated `docs/TROUBLESHOOTING.md` with GPIO4/SD troubleshooting

## 0.3.1 - Phase 2C: Trigger + Capture Logic

### Added

- `firmware/lib/trigger_controller.py` — TriggerController class: threshold (50cm), cooldown (15s), `should_trigger()` with `time.ticks_ms()` based timing
- `firmware/test_trigger_capture.py` — standalone test: sensor → trigger → camera → save (motion_001.jpg, motion_002.jpg, ...)

### Notes

- Cooldown prevents repeated captures from the same event
- Filename counter resets per test run
- Ctrl+C prints summary (readings + captures)
- No SD card, Telegram, or cloud integration yet

## 0.3.0 - Phase 2A: HC-SR04 Sensor Test

### Added

- `firmware/lib/sensor_hcsr04.py` — HC-SR04 driver: TRIG=GPIO12, ECHO=GPIO13, echo timeout, distance in cm
- `firmware/test_hcsr04.py` — standalone sensor test: reads every 1s, Ctrl+C to stop

### Wiring

- TRIG → GPIO 12, ECHO → voltage divider (1kΩ + 2kΩ) → GPIO 13
- CRITICAL: 5V ECHO must go through divider to 3.3V GPIO

### Notes

- Isolated test — no camera/wifi integration yet
- Uses `machine.time_pulse_us()` for echo measurement
- 30ms echo timeout, 400cm max range
- Camera init fixed: 1 positional arg only (`camera.init(framesize)`)

## 0.2.2 - Phase 1 Code (LeMaRiva API fix)

### Changed

- `firmware/lib/camera_manager.py` — fixed to single positional arg: `camera.init(framesize)`
- `firmware/lib/wifi_manager.py` — skips Wi-Fi if config.py has placeholder credentials
- `firmware/main.py` — Wi-Fi is optional (SKIP if no config); PASS/FAIL/SKIP per step

### Notes

- Camera init verified working on ESP32-D0WD-V3 with LeMaRiva `micropython_camera_feeeb5ea3_esp32_idf4_4.bin`
- Upload with Thonny (right-click → Upload to /)

## 0.2.1 - Phase 1 Camera Verification PASSED

- `import camera` PASS
- `camera.init(0, format=camera.JPEG, fb_location=camera.PSRAM)` returned True
- `camera.capture()` returned 7102 bytes
- `test.jpg` saved successfully

## 0.2.0 - Phase 1 Firmware Bring-Up

### Added

- `firmware/boot.py`, `firmware/config.example.py`
- `firmware/lib/logger.py`, `wifi_manager.py`, `camera_manager.py`
- `firmware/main.py` — Phase 1 orchestrator
- `firmware_bin/` — LeMaRiva firmware binary + README
- `tools/flash_firmware.ps1` — Windows flash script
- `docs/FLASHING_GUIDE.md` — Windows flashing guide

## 0.1.0 - Initial Documentation Pack

Documentation only. No implementation.
