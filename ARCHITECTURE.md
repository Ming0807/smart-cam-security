# Architecture

## Recommended Stable Architecture

```text
[Object detected under threshold]
        ↓
[HC-SR04]
        ↓
[ESP32-CAM with MicroPython]
        ├─ Measure distance
        ├─ Capture JPEG
        ├─ Save JPEG to MicroSD
        ├─ Send Telegram alert
        ├─ POST event to Next.js API
        └─ Poll cloud commands

[Next.js on Vercel]
        ├─ Dashboard UI
        ├─ API Routes
        ├─ Telegram callback endpoint
        └─ Supabase client/server integration

[Supabase PostgreSQL]
        ├─ system_config
        ├─ event_logs
        ├─ device_commands
        └─ command_results

[Home Gateway]
        ├─ Optional reverse proxy
        ├─ Cloudflare Tunnel or ngrok
        └─ Remote stream access
```

## Responsibility Split

### ESP32-CAM

The device is responsible for:

- Sensor reading
- Trigger decision
- Camera snapshot
- SD card storage
- Telegram alert
- Sending log to cloud
- Polling commands from cloud

The device is not responsible for:

- Running Cloudflare Tunnel
- Hosting a public dashboard
- Generating long video streams for cloud proxy
- Running heavy video processing

### Next.js / Vercel

The web app is responsible for:

- Dashboard pages
- API routes
- System status management
- Command queue
- Telegram callback handling
- Supabase integration

The web app is not responsible for:

- Long-running MJPEG stream proxy
- Directly connecting into local ESP32-CAM behind NAT
- Storing large video files in serverless functions

### Supabase

The database is responsible for:

- System configuration
- Event logs
- Device command queue
- Command execution result logs

### Home Gateway

The gateway is responsible for optional remote access to the local camera stream.

Recommended devices:

- Notebook
- Desktop PC
- Raspberry Pi
- Mini PC

Recommended tunnel services:

- Cloudflare Tunnel with custom domain for production
- Cloudflare Quick Tunnel for temporary testing
- ngrok free dev domain for quick stable demo URL

## Command Polling Flow

```text
User clicks Disarm in dashboard
  ↓
Next.js API inserts command into Supabase
  ↓
ESP32-CAM polls /api/commands
  ↓
ESP32-CAM receives pending command
  ↓
ESP32-CAM executes command
  ↓
ESP32-CAM posts result to /api/commands/result
  ↓
Dashboard shows updated state
```

## Event Alert Flow

```text
Object detected
  ↓
ESP32-CAM captures JPEG
  ↓
ESP32-CAM saves JPEG to SD
  ↓
ESP32-CAM sends Telegram text
  ↓
ESP32-CAM sends Telegram photo
  ↓
ESP32-CAM posts event log to API
  ↓
Supabase stores event
  ↓
Dashboard displays event
```

## Why Not Vercel Stream Proxy?

Vercel serverless functions are not suitable for long-running camera streams. Use Vercel for dashboard and APIs only.

## Why Command Polling?

ESP32-CAM is usually behind NAT. Direct inbound access is unstable and may require port forwarding. Polling allows the device to initiate outbound HTTPS requests, which is more reliable.
