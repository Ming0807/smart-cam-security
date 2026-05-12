# Next Tasks

## Current Phase

Phase 4C: Trigger + Capture + Save to SD — Code ready.

## Verified So Far

| Component | Status |
|---|---|
| Wi-Fi | PASS |
| Camera + capture | PASS |
| HC-SR04 sensor | PASS |
| Trigger + cooldown | PASS |
| Flash LED (GPIO4) | PASS |
| Telegram text alert | PASS |
| Full pipeline (sensor→Telegram→capture) | PASS |
| MicroSD mount + read/write | PASS |
| Camera → SD save | PASS |
| Trigger → Camera → SD (no Wi-Fi/flash) | READY |

## Active Task: Upload and Run

1. Upload via Thonny:
   - `firmware/lib/local_event_storage.py` → `/lib/`
   - `firmware/test_trigger_save_sd.py` → `/`
2. Power-cycle the board before running (remove old main.py interference)
3. Run: `import test_trigger_save_sd`
4. Test:
   - No object → no capture
   - Object near (< 50cm) → capture → `motion_sd_YYYYMMDD_HHMMSS.jpg` on /sd
   - Cooldown prevents spam
   - Ctrl+C clean stop

## SD Mount Rule (IMPORTANT)

SD card must be mounted **before** camera init. Camera init installs GPIO ISR which blocks SD detection.

Order: `SD mount` → `camera init` → `trigger loop`

## Next Phase

Phase 5: Next.js API + Supabase

## Do Not Work On Yet

AVI recording, live streaming
