# Best Practices

## MicroPython Best Practices

- Keep the main loop simple.
- Use clear state flags: `is_armed`, `is_muted`, `last_trigger_time`.
- Use cooldown after detection to avoid repeated alerts.
- Use timeouts for sensor echo reading.
- Use timeouts for HTTP requests.
- Limit Telegram retries.
- Free camera buffers after sending/saving when possible.
- Do not hold large image data in memory longer than necessary.
- Prefer JPEG snapshot for MVP.
- Store files with timestamp names.

## ESP32-CAM Stability

- Use a stable 5V 2A power supply.
- Avoid powering camera and sensor from weak USB adapters.
- Use short jumper wires where possible.
- Use voltage divider on HC-SR04 Echo.
- Confirm PSRAM availability if using high-resolution photos.
- Start with low or medium resolution before increasing quality.

## HC-SR04 Best Practices

- Use 5V for sensor power.
- Use voltage divider on Echo to ESP32 GPIO.
- Add echo timeout.
- Filter readings using median or moving average if noisy.
- Use trigger threshold plus cooldown.

## SD Card Best Practices

- Use FAT32.
- Use reliable branded MicroSD.
- Avoid constant writes in tight loop.
- Use timestamp filenames.
- Implement FIFO cleanup.
- Check free space before saving.

## Telegram Bot Best Practices

- Send message first, then photo.
- Keep messages short and useful.
- Do not send large videos in MVP.
- Add inline buttons only after base alerts work.
- Handle failed Telegram requests gracefully.

## Next.js Best Practices

- Keep API routes focused.
- Validate request payloads.
- Return structured JSON.
- Use environment variables.
- Keep dashboard pages simple in MVP.
- Separate UI components from API logic.
- Avoid using serverless API routes as camera stream proxy.

## Supabase Best Practices

- Use PostgreSQL tables for event logs and commands.
- Use RLS carefully.
- Never expose service role key to browser.
- Use indexes on timestamp and command status.
- Keep command queue simple.

## Security Best Practices

- Use different secrets for device API and Telegram.
- Rotate tokens if accidentally exposed.
- Do not hardcode real credentials in committed files.
- Protect dashboard before real deployment.
- Avoid public access to device command endpoints without secret validation.

## Agent Best Practices

- Read docs before editing.
- Work one phase at a time.
- Do not over-engineer.
- Update changelog.
- Add troubleshooting notes when errors appear.
