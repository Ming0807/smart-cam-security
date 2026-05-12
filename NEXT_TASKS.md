# Next Tasks

## Current Phase

Phase 4D: Full Pipeline (Telegram + SD) — Code ready.

## Verified So Far

| Component | Status |
|---|---|
| Wi-Fi | PASS |
| Camera + capture | PASS |
| HC-SR04 sensor | PASS |
| Trigger + cooldown | PASS |
| Flash LED (GPIO4) | PASS |
| Telegram text | PASS |
| Telegram photo | READY |
| MicroSD mount (slot=1 width=1) | PASS |
| Camera → save to SD | PASS |
| Trigger → Camera → SD | PASS |
| Trigger → Telegram → Camera → SD → Telegram photo | READY |

## Active Task: Upload and Run

1. Power-cycle board
2. Upload via Thonny:
   - `firmware/lib/full_alert_workflow.py` → `/lib/`
   - `firmware/lib/telegram_client.py` → `/lib/` (updated with send_photo)
   - `firmware/test_full_local_alert_sd.py` → `/`
3. Run: `import test_full_local_alert_sd`
4. Test:
   - Object near → Telegram text → capture → SD save → Telegram photo
   - Check Telegram for both text and photo messages
   - Check SD for motion_sd_*.jpg files
   - Cooldown prevents spam
   - If photo fails, SD image still saved

## Next Phase

Phase 5: Next.js API + Supabase (web dashboard)

## Do Not Work On Yet

AVI recording, live streaming
