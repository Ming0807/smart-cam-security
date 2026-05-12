# Next Tasks

## Current Phase

Phase 2D: Flash LED Test — Code ready. Upload + run pending.

## Verified So Far

| Component | Status |
|---|---|
| Wi-Fi | PASS |
| Camera (init, capture, save) | PASS |
| HC-SR04 sensor | PASS |
| Trigger + capture (threshold 50cm, cooldown 15s) | PASS |
| Flash LED (GPIO4) | READY |

## Active Task: Upload and Run flash LED test

1. Upload via Thonny:
   - `firmware/lib/flash_led.py` → `/lib/`
   - `firmware/test_flash_led.py` → `/`
2. In REPL, run: `import test_flash_led`
3. Verify: flash LED blinks 3 times briefly (200ms each)
4. Confirm LED is OFF after test completes
5. Note: GPIO4 conflicts with SD card 4-bit mode — remove SD or use 1-bit mode

## Next Phase

Phase 3: SD Card Storage
- Mount MicroSD (FAT32) in 1-bit mode to free GPIO4/12/13
- Save JPEG with timestamp filename to SD
- FIFO cleanup when space low

## Do Not Work On Yet

Telegram, Supabase, Next.js dashboard, AVI recording, live streaming
