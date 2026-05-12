# Smart Security Camera

Smart Security Camera with Ultrasonic Trigger, Telegram Alert, Next.js Dashboard, Supabase Database, and optional Remote Stream Gateway.

## Project Summary

This project uses an AI-Thinker ESP32-CAM running MicroPython to detect nearby objects using an HC-SR04 ultrasonic sensor. When an object is detected, the device captures a JPEG snapshot, saves it to MicroSD, sends a Telegram alert, and posts an event log to a Next.js API deployed on Vercel.

The dashboard is built with Next.js App Router and stores system status, event logs, and commands in Supabase PostgreSQL.

## Important Constraint

The ESP32-CAM firmware must use MicroPython only.

Do not rewrite the firmware in Arduino C++ or ESP-IDF unless the project owner explicitly changes this requirement.

## Recommended Stable Architecture

```text
HC-SR04
  ↓
ESP32-CAM MicroPython
  ├─ Read distance
  ├─ Capture JPEG snapshot
  ├─ Save media to MicroSD
  ├─ Send Telegram alert
  ├─ POST event log to Next.js API
  └─ Poll cloud commands

Next.js on Vercel
  ├─ Dashboard
  ├─ API Routes
  ├─ Command Queue
  └─ Supabase Integration

Supabase
  ├─ system_config
  ├─ event_logs
  ├─ device_commands
  └─ command_results

Home Gateway
  └─ Cloudflare Tunnel / ngrok for remote stream access
```

## MVP Scope

The first stable version should include:

- Wi-Fi connection from ESP32-CAM
- HC-SR04 distance reading
- JPEG snapshot capture
- Save JPEG to MicroSD
- Telegram text alert
- Telegram photo alert
- Event log API
- Supabase event log storage
- Dashboard event list
- Arm / Disarm system status
- Command polling from ESP32-CAM

## Out of Scope for MVP

Do not implement these in the first version:

- AVI video recording
- Large video upload to Telegram
- Long-running MJPEG proxy through Vercel
- Direct inbound commands from Vercel to ESP32-CAM
- ESP32-CAM running Cloudflare Tunnel directly

## Documentation Map

| File | Purpose |
|---|---|
| `AGENTS.md` | Main rules for coding agents |
| `PROJECT_BLUEPRINT.md` | Full project blueprint |
| `ARCHITECTURE.md` | Stable system architecture |
| `DEVELOPMENT_RULES.md` | Daily development rules |
| `BEST_PRACTICES.md` | Practical best practices |
| `TASKS.md` | Full backlog |
| `NEXT_TASKS.md` | Current active work |
| `docs/FIRMWARE_MICROPYTHON_SPEC.md` | ESP32-CAM firmware spec |
| `docs/NEXTJS_API_SPEC.md` | API routes spec |
| `docs/DATABASE_SCHEMA.md` | Supabase schema |
| `docs/SECURITY.md` | Security rules |
| `docs/skills/` | Skill files for agents |
| `.opencode/agents/` | OpenCode custom agents |
| `.opencode/commands/` | OpenCode custom commands |

## Suggested First Command for OpenCode

After opening this folder in OpenCode Agent Desktop, start with:

```text
Read AGENTS.md, PROJECT_BLUEPRINT.md, ARCHITECTURE.md, TASKS.md, and NEXT_TASKS.md.
Then create an implementation plan for the active task only.
```
