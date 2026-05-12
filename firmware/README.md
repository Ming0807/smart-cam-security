# Firmware Folder

ESP32-CAM MicroPython firmware files.

## File Structure

```
firmware/
  boot.py                  # Minimal boot: garbage collection only
  main.py                  # Phase 1: Wi-Fi + camera test, saves test.jpg
  config.example.py        # Template (copy to config.py, fill real SSID/PW)
  lib/
    logger.py              # Console logger with timestamps
    wifi_manager.py        # Wi-Fi connect with timeout + retry
    camera_manager.py      # Camera init, JPEG capture, save, deinit
```

## How to Upload (mpremote — recommended)

Install mpremote:
```
pip install mpremote
```

Upload all files to ESP32-CAM:
```
mpremote connect COM13 fs cp firmware/boot.py :boot.py
mpremote connect COM13 fs cp firmware/main.py :main.py
mpremote connect COM13 fs cp firmware/config.py :config.py
mpremote connect COM13 fs mkdir :lib
mpremote connect COM13 fs cp firmware/lib/logger.py :lib/logger.py
mpremote connect COM13 fs cp firmware/lib/wifi_manager.py :lib/wifi_manager.py
mpremote connect COM13 fs cp firmware/lib/camera_manager.py :lib/camera_manager.py
```

Replace `COM13` with your actual port.

## How to Upload (Thonny)

1. Open Thonny, select MicroPython (ESP32), correct COM port.
2. Copy `config.example.py` → `config.py`, fill Wi-Fi SSID/password.
3. Right-click each file → "Upload to /".
4. Create `lib/` folder on device, upload the three library files.
5. Press reset or run `import main` in REPL.

## How to Run

In REPL:
```python
import main
```

Or reset the board — `main.py` runs automatically on startup.

## Expected Output

```
[2026-05-12 12:00:00] === Phase 1: Firmware Bring-Up ===
[2026-05-12 12:00:00] MicroPython version: v1.22.2
[2026-05-12 12:00:00] Free memory: 3456789 bytes
[2026-05-12 12:00:01] Connecting to: MyWiFi
[2026-05-12 12:00:03] Connected! IP: 192.168.1.100
[2026-05-12 12:00:03] PASS: Wi-Fi connected
[2026-05-12 12:00:03] Camera module loaded
[2026-05-12 12:00:03] Camera ready (framesize=8, quality=10)
[2026-05-12 12:00:03] PASS: Camera initialized
[2026-05-12 12:00:04] Captured 24567 bytes
[2026-05-12 12:00:04] PASS: JPEG captured (24567 bytes)
[2026-05-12 12:00:04] Saved: test.jpg
[2026-05-12 12:00:04] PASS: test.jpg saved
[2026-05-12 12:00:04] === Phase 1 Complete ===
[2026-05-12 12:00:04] Wi-Fi:   PASS
[2026-05-12 12:00:04] Camera:  PASS
[2026-05-12 12:00:04] Output:  test.jpg saved to device
```

Each step prints PASS or FAIL so you can see exactly what worked and what didn't.

## Troubleshooting

| Problem | Fix |
|---|---|
| `import camera` → ImportError | Flash camera-enabled firmware |
| Camera init → reboot | Use 5V 2A power, check ribbon cable |
| Wi-Fi timeout | 2.4 GHz only, check SSID/password |
| config.py not found | Copy config.example.py → config.py |

See `docs/TROUBLESHOOTING.md` for more.
