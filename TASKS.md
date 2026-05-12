# Tasks

## Phase 0: Project Setup

- [ ] Create repository structure
- [ ] Add documentation files
- [ ] Add `.env.example`
- [ ] Add `.gitignore`
- [ ] Confirm hardware list
- [ ] Confirm development machine tools

## Phase 1: Firmware Bring-Up

- [ ] Flash camera-enabled MicroPython firmware
- [ ] Confirm REPL access in Thonny
- [ ] Test `import camera`
- [ ] Initialize camera
- [ ] Capture one JPEG snapshot
- [ ] Connect to Wi-Fi
- [ ] Print local IP address
- [ ] Save Wi-Fi config outside committed code

## Phase 2: Sensor and SD Card

- [ ] Wire HC-SR04 with voltage divider
- [ ] Test distance reading
- [ ] Add echo timeout
- [ ] Add distance smoothing/filtering
- [ ] Mount MicroSD
- [ ] Save test text file to SD
- [ ] Save JPEG snapshot to SD
- [ ] Implement timestamp filename

## Phase 3: Trigger Logic

- [ ] Add arm/disarm state
- [ ] Add trigger threshold
- [ ] Add trigger cooldown
- [ ] Capture JPEG when object detected
- [ ] Save event image to SD
- [ ] Add basic local logging
- [ ] Prevent alert spam

## Phase 4: Telegram Alert

- [ ] Create Telegram bot
- [ ] Get Telegram chat ID
- [ ] Send text message from ESP32-CAM
- [ ] Send JPEG photo from ESP32-CAM
- [ ] Add retry and timeout
- [ ] Add useful message format
- [ ] Store token securely

## Phase 5: Next.js API and Supabase

- [ ] Create Next.js App Router project
- [ ] Connect Supabase
- [ ] Create database schema
- [ ] Add `/api/log`
- [ ] Add `/api/status`
- [ ] Add `/api/commands`
- [ ] Add `/api/commands/result`
- [ ] Validate ESP32 requests with `X-Device-Secret`

## Phase 6: Dashboard MVP

- [ ] Create dashboard home page
- [ ] Show system status
- [ ] Show event log table
- [ ] Add Arm / Disarm switch
- [ ] Add manual refresh
- [ ] Add basic responsive UI
- [ ] Add empty state and error state

## Phase 7: Command Polling

- [ ] ESP32 polls `/api/status`
- [ ] ESP32 polls `/api/commands`
- [ ] Execute command: `arm`
- [ ] Execute command: `disarm`
- [ ] Execute command: `mute`
- [ ] Execute command: `unmute`
- [ ] Report command result
- [ ] Mark commands as done or failed

## Phase 8: Telegram Inline Buttons

- [ ] Add dashboard link button
- [ ] Add disarm button
- [ ] Add mute button
- [ ] Add Telegram callback endpoint
- [ ] Convert callback into cloud command
- [ ] Confirm command execution by ESP32

## Phase 9: SD Cleanup

- [ ] Check SD free space
- [ ] List media files
- [ ] Sort files by timestamp
- [ ] Delete oldest file when below threshold
- [ ] Log deleted files
- [ ] Add cleanup test notes

## Phase 10: Optional Remote Stream

- [ ] Test local snapshot endpoint
- [ ] Set up home gateway
- [ ] Test Cloudflare Quick Tunnel
- [ ] Test ngrok dev domain
- [ ] Add dashboard stream link
- [ ] Document tunnel setup

## Phase 11: Advanced Evidence

- [ ] Add JPEG burst capture
- [ ] Save burst folder per event
- [ ] Optional MJPEG sequence
- [ ] Optional gateway-side video assembly
- [ ] Optional Telegram video upload

## Phase 12: Production Hardening

- [ ] Add dashboard authentication
- [ ] Add RLS policies
- [ ] Add health check endpoint
- [ ] Add device heartbeat
- [ ] Add watchdog/recovery strategy
- [ ] Add deployment checklist
- [ ] Add final test report
