# AGENTS.md

## Project Overview

This project is a Smart Security Camera system using:

- ESP32-CAM AI-Thinker
- MicroPython firmware with camera support
- HC-SR04 ultrasonic sensor
- MicroSD local storage
- Telegram Bot alert
- Next.js App Router dashboard
- Vercel deployment
- Supabase PostgreSQL database
- Optional Cloudflare Tunnel or ngrok through a home gateway

## Hard Constraints

These rules must not be violated.

1. ESP32-CAM firmware must use MicroPython only.
2. Do not rewrite firmware in Arduino C++.
3. Do not rewrite firmware in ESP-IDF.
4. Do not use Vercel as a long-running MJPEG stream proxy.
5. Do not assume ESP32-CAM can run Cloudflare Tunnel or ngrok directly.
6. Use command polling for remote control instead of direct inbound access to ESP32-CAM.
7. Start with JPEG snapshot capture before attempting burst capture, MJPEG, or AVI.
8. Do not expose secrets in client-side code or committed files.
9. Do not change hardware pins without updating `docs/PIN_MAPPING.md`.
10. Do not change database schema without updating `docs/DATABASE_SCHEMA.md`.

## Required Reading Before Any Work

Before making changes, read:

1. `PROJECT_BLUEPRINT.md`
2. `ARCHITECTURE.md`
3. `DEVELOPMENT_RULES.md`
4. `TASKS.md`
5. `NEXT_TASKS.md`
6. Relevant files in `docs/`

## Development Workflow

Before editing code:

1. Identify the current active task from `NEXT_TASKS.md`.
2. Work only on that task.
3. Avoid unrelated refactors.
4. Make the smallest useful change.
5. Update relevant documentation if behavior changes.
6. Update `CHANGELOG.md` after implementation.
7. Add troubleshooting notes if a new problem is found.

## Architecture Rule

The stable architecture is:

```text
ESP32-CAM = detection + capture + SD storage + Telegram + cloud polling
Next.js/Vercel = dashboard + API routes + command queue
Supabase = database
Gateway = remote stream tunnel
Telegram = alert and quick commands
```

## Firmware Rules

- Use MicroPython only.
- Use a camera-enabled MicroPython build.
- Keep memory use low.
- Add timeouts to network calls.
- Use retry with limited attempts.
- Do not keep large image buffers in RAM longer than needed.
- Prefer JPEG snapshot for MVP.
- Treat AVI recording as advanced work only.

## Next.js Rules

- Use App Router.
- Keep API routes small.
- Validate request payloads.
- Use environment variables.
- Never expose Supabase service role key to browser/client components.
- Do not proxy long-running camera streams through Vercel.

## Database Rules

- Use Supabase PostgreSQL.
- Keep schema simple.
- Use `system_config`, `event_logs`, `device_commands`, and `command_results`.
- Device commands should have status: `pending`, `processing`, `done`, `failed`.

## Security Rules

- ESP32-CAM must authenticate with an API secret.
- Telegram tokens must stay in environment variables or device secret files.
- Do not commit `.env.local`, secrets, Wi-Fi passwords, or bot tokens.
- Dashboard control actions must require authentication in production.

## Response Format for Agents

After completing a task, report:

```text
Changed files:
- file path
- what changed

Tests:
- what was tested
- result

Notes:
- risks
- follow-up tasks
```
