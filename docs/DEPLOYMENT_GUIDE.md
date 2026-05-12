# Deployment Guide

## Local Development

### Requirements

- Node.js LTS
- Git
- Supabase account
- Vercel account
- Telegram account
- Thonny IDE
- ESP32-CAM-MB or USB-to-serial adapter

## Next.js Setup

Planned commands:

```bash
npx create-next-app@latest web
cd web
npm install @supabase/supabase-js
npm run dev
```

## Environment Setup

Create `.env.local` based on `.env.example`.

Never commit `.env.local`.

## Supabase Setup

1. Create Supabase project.
2. Open SQL editor.
3. Run SQL from `docs/DATABASE_SCHEMA.md`.
4. Copy project URL and anon key.
5. Copy service role key for server-side API only.

## Vercel Deployment

1. Push repository to GitHub.
2. Import project into Vercel.
3. Add environment variables.
4. Deploy.
5. Test API routes.

## Telegram Setup

1. Create bot with BotFather.
2. Copy bot token.
3. Get chat ID.
4. Store token and chat ID securely.
5. Test message send.

## ESP32-CAM Setup

1. Flash camera-enabled MicroPython firmware.
2. Open Thonny.
3. Confirm REPL.
4. Upload firmware files.
5. Test camera.
6. Test sensor.
7. Test Wi-Fi.
8. Test Telegram.

## Optional Tunnel Setup

### Cloudflare Quick Tunnel

For temporary demo:

```bash
cloudflared tunnel --url http://localhost:8080
```

### ngrok

For dev domain:

```bash
ngrok http 8080
```

## Production Checklist

- [ ] Secrets stored in Vercel env
- [ ] Device secret configured
- [ ] Telegram token not committed
- [ ] Supabase service role key not exposed
- [ ] Dashboard auth considered
- [ ] ESP32-CAM stable power supply
- [ ] Sensor voltage divider installed
- [ ] SD card tested
