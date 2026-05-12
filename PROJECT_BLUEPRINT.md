# Project Blueprint

## Project Name

Smart Security Camera with Ultrasonic Trigger, Telegram Alert, and Next.js Dashboard

## Goal

Build a stable, free, and practical smart camera security system using ESP32-CAM with MicroPython. The system detects nearby objects using HC-SR04, captures a snapshot, saves evidence to MicroSD, sends Telegram alerts, and displays event logs in a Next.js dashboard.

## Primary Requirements

### Hardware Detection

- Continuously measure distance using HC-SR04.
- Trigger when distance is below a configurable threshold.
- Default threshold: 50 cm.
- Support arm/disarm status from cloud.

### Camera Capture

- Capture JPEG snapshot after trigger.
- Save JPEG to MicroSD card.
- Use timestamp-based filename.
- Future support: JPEG burst, MJPEG sequence, optional video assembly.

### Local Storage

- Store evidence files on MicroSD FAT32.
- Implement FIFO cleanup when free space is too low.
- Default low-space threshold: 500 MB.

### Telegram Alert

- Send real-time text message.
- Send first snapshot as photo.
- Include event details:
  - timestamp
  - distance
  - device id
  - image filename
- Include inline buttons:
  - Open Dashboard
  - Disarm
  - Mute
  - Delete latest file

### Web Dashboard

- Built with Next.js App Router.
- Deployed on Vercel.
- Shows event logs from Supabase.
- Shows system status.
- Allows Arm / Disarm.
- Sends commands through a command queue.

### Database

Use Supabase PostgreSQL.

Main tables:

- `system_config`
- `event_logs`
- `device_commands`
- `command_results`

### Remote Stream

Live stream is not part of MVP.

Recommended later architecture:

```text
ESP32-CAM local stream
  ↓
Home Gateway: PC / Notebook / Raspberry Pi
  ↓
Cloudflare Tunnel or ngrok
  ↓
Public HTTPS URL
  ↓
Dashboard link or embedded viewer
```

## MVP Features

- ESP32-CAM connects to Wi-Fi.
- ESP32-CAM reads HC-SR04 distance.
- ESP32-CAM captures JPEG.
- ESP32-CAM saves JPEG to SD.
- ESP32-CAM sends Telegram message.
- ESP32-CAM sends Telegram photo.
- ESP32-CAM posts event log to API.
- Next.js API stores event in Supabase.
- Dashboard lists events.
- Dashboard controls arm/disarm.
- ESP32-CAM polls cloud command/status.

## Advanced Features

These should be implemented only after MVP is stable.

- JPEG burst capture
- MJPEG sequence storage
- Gateway-side MP4/AVI generation
- Remote live stream through tunnel
- User authentication
- Media gallery
- File delete command
- Multi-device support
- Health monitoring
- Watchdog/recovery

## Non-Goals

The following are intentionally not required for MVP:

- Full CCTV-grade video recording
- Always-on video cloud recording
- Vercel-based video streaming proxy
- Port forwarding at router
- ESP32-CAM running tunnel client directly
