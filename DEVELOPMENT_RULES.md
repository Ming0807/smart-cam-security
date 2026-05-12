# Development Rules

## General Rules

- Work in small, testable steps.
- Do not edit unrelated files.
- Do not introduce major refactors during feature implementation.
- Do not change architecture silently.
- Update documentation when behavior changes.
- Keep the MVP stable before adding advanced features.
- Prefer working code over clever code.

## Phase Discipline

Always check `NEXT_TASKS.md`.

Only implement the active task.

Do not work on:

- AVI recording
- live streaming
- tunnel integration
- Telegram inline keyboard
- advanced dashboard pages

unless they are listed as the active task.

## Firmware Rules

- Use MicroPython only.
- Do not generate Arduino C++ code.
- Do not generate ESP-IDF code.
- Use camera-enabled MicroPython firmware.
- Avoid memory-heavy patterns.
- Use timeouts for network requests.
- Use retry with a maximum attempt count.
- Use simple functions and clear state variables.
- Always clean up large buffers when possible.
- Keep trigger cooldown to avoid alert spam.

## Hardware Rules

- Respect `docs/PIN_MAPPING.md`.
- Do not assign GPIO 13 to Echo without voltage divider.
- Do not change SD card mode without documenting the impact.
- Do not assume all ESP32-CAM boards expose the same pins.

## Web Rules

- Use Next.js App Router.
- Keep API logic small and predictable.
- Validate all incoming data.
- Use server-side Supabase client for secret operations.
- Use client-side Supabase only with safe public anon key.
- Store secrets in environment variables.
- Never expose service role key in client code.

## Database Rules

- Update `docs/DATABASE_SCHEMA.md` for schema changes.
- Use migrations or SQL files where possible.
- Do not delete columns without migration notes.
- Keep command statuses explicit.

## Security Rules

- No secrets in Git.
- No Telegram bot token in committed firmware.
- No Wi-Fi password in committed firmware.
- Use `.env.example` as template only.
- Use `X-Device-Secret` for device API calls.
- In production, protect dashboard control pages.

## Testing Rules

Each task must include a test note.

Examples:

- Firmware import test
- Wi-Fi connection test
- Sensor distance reading test
- Snapshot capture test
- SD save test
- Telegram text send test
- API POST test
- Dashboard render test

## Documentation Rule

Update the relevant documentation when the implementation changes any of these:

- pin mapping
- API request/response
- database schema
- firmware behavior
- environment variables
- deployment steps
- known bugs
