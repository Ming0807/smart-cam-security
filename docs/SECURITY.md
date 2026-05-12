# Security

## Secret Management

Never commit:

- Wi-Fi SSID
- Wi-Fi password
- Telegram bot token (stored in `firmware/config.py`)
- Telegram chat ID (stored in `firmware/config.py`)
- Supabase service role key
- Device API secret
- Tunnel credentials

Use:

- `.env.local` for local Next.js secrets
- Vercel environment variables for production
- ignored MicroPython config files for device secrets

## Required Environment Variables

```text
NEXT_PUBLIC_SUPABASE_URL
NEXT_PUBLIC_SUPABASE_ANON_KEY
SUPABASE_SERVICE_ROLE_KEY
DEVICE_API_SECRET
TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID
NEXT_PUBLIC_SITE_URL
```

## Device Authentication

ESP32-CAM must send:

```http
X-Device-Secret: <secret>
```

Next.js API routes must reject unauthorized requests.

## Telegram Security

- Keep bot token private.
- Validate callback data.
- Do not allow arbitrary command payloads from Telegram.
- Convert callback data only into known allowed commands.

## Dashboard Security

For MVP, dashboard may be simple.

For production:

- Add authentication.
- Protect control actions.
- Add rate limiting where possible.
- Avoid public write access.

## Supabase Security

- Never expose service role key to client components.
- Use anon key only for safe public reads if needed.
- Enable RLS before public launch.
- Use API routes for privileged operations.

## Tunnel Security

If using Cloudflare Tunnel or ngrok:

- Do not expose unnecessary local services.
- Expose only the camera proxy or dashboard route needed.
- Prefer authenticated access for production.
- Keep tunnel credentials private.
