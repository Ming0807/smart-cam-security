# Test Plan

## Phase 1: Firmware Bring-Up

### Camera Verification — PASSED (2026-05-12)

ESP32-D0WD-V3 + LeMaRiva `micropython_camera_feeeb5ea3_esp32_idf4_4.bin`

| # | Test | Actual | Status |
|---|---|---|---|
| 1 | `print("hello")` | OK | PASS |
| 2 | `import camera` | No error | PASS |
| 3 | `camera.init(5)` | True | PASS |
| 4 | `camera.capture()` | Returns bytes | PASS |
| 5 | Save JPEG | File saved | PASS |

### Full Phase 1 Sequence

| # | Test | Expected | Status |
|---|---|---|---|
| 1 | `import main` | Full sequence runs | PASS |
| 2 | Wi-Fi connect | `Connected! IP: 192.168.x.x` | PASS |
| 3 | Camera init | `Camera ready` | PASS |
| 4 | Capture | `Captured N bytes` | PASS |
| 5 | Save test.jpg | `Saved: test.jpg` | PASS |

## Phase 2A: HC-SR04 Sensor Test

### Wiring

```
HC-SR04 VCC  -> ESP32-CAM 5V
HC-SR04 GND  -> ESP32-CAM GND
HC-SR04 TRIG -> GPIO 12
HC-SR04 ECHO -> voltage divider (1kΩ + 2kΩ) -> GPIO 13
```

| # | Test | Expected | Status |
|---|---|---|---|
| 1 | `import lib.sensor_hcsr04` | No error | PASS |
| 2 | `import test_hcsr04` | Test starts | PASS |
| 3 | No object near | `OUT OF RANGE` | PASS |
| 4 | Object at ~30 cm | `~30 cm` | PASS |
| 5 | Ct rl+C | `Test stopped` | PASS |

## Phase 2C: Trigger + Capture

| # | Test | Expected | Status |
|---|---|---|---|
| 1 | `import lib.trigger_controller` | No error | PENDING |
| 2 | `import test_trigger_capture` | Test starts | PENDING |
| 3 | Object far (> 50 cm) | No trigger, prints `armed` | PENDING |
| 4 | Object near (< 50 cm) | `TRIGGER!` → capture → `motion_001.jpg` | PENDING |
| 5 | Object stays near | `cooldown Xs remaining` — no duplicate | PENDING |
| 6 | Wait cooldown, object near again | Second trigger → `motion_002.jpg` | PENDING |
| 7 | Ctrl+C | Summary: N readings, M captures | PENDING |

## Phase 2D: Flash LED (GPIO4)

| # | Test | Expected | Status |
|---|---|---|---|
| 1 | `import lib.flash_led` | No error | PENDING |
| 2 | `import test_flash_led` | Test starts | PENDING |
| 3 | Flash blinks 3 times | 3 brief pulses visible (200ms each) | PENDING |
| 4 | LED OFF after test | LED stays off | PENDING |
| 5 | Ctrl+C during test | LED turns OFF cleanly | PENDING |

GPIO4 conflict note: remove MicroSD or use 1-bit SD mode.

## Phase 3: SD Card

| Test | Expected |
|---|---|
| SD mount | Mount succeeds |
| Write text file | File on SD |
| Save JPEG to SD | JPEG with timestamp filename |

## Phase 4: Telegram

| Test | Expected |
|---|---|
| Send text | Message in chat |
| Send photo | Image in chat |
| Invalid token | Error handled |

## Phase 5: API

| Test | Expected |
|---|---|
| POST `/api/log` with secret | 200 |
| POST `/api/log` without secret | 401 |
| GET `/api/status` | JSON |

## Phase 6: Dashboard

| Test | Expected |
|---|---|
| Dashboard loads | No crash |
| Event logs visible | Rows |
| Arm/Disarm | Status changes |

## Final Acceptance

1. Detect object under 50 cm → capture JPEG → save to SD
2. Telegram alert (text + photo)
3. Event in dashboard
4. Dashboard disarm respected
