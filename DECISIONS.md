# Architecture Decisions

## ADR-001: Use MicroPython for ESP32-CAM Firmware

### Status

Accepted

### Context

The project owner requires MicroPython only for the ESP32-CAM firmware.

### Decision

All firmware running on ESP32-CAM must be written in MicroPython.

### Consequences

- Need camera-enabled MicroPython firmware.
- Camera support may depend on community/custom firmware.
- AVI recording is treated as advanced and risky.
- MVP focuses on JPEG snapshot capture.

---

## ADR-002: Use Next.js on Vercel for Dashboard and API

### Status

Accepted

### Context

The project needs a free and easy web deployment path.

### Decision

Use Next.js App Router and deploy to Vercel.

### Consequences

- Good for dashboard and API routes.
- Not suitable for long-running MJPEG stream proxy.
- Use Supabase for persistent database.

---

## ADR-003: Use Supabase PostgreSQL

### Status

Accepted

### Context

The system needs persistent cloud storage for status, events, and commands.

### Decision

Use Supabase PostgreSQL Free plan for MVP.

### Consequences

- Simple SQL schema.
- Easy integration with Next.js.
- Must protect service role key.

---

## ADR-004: Use Command Polling

### Status

Accepted

### Context

ESP32-CAM is behind home NAT and direct inbound access is unstable.

### Decision

ESP32-CAM polls the cloud for commands.

### Consequences

- No router port forwarding needed.
- Dashboard and Telegram can create commands.
- ESP32-CAM executes commands during polling loop.

---

## ADR-005: Do Not Use Vercel as Camera Stream Proxy

### Status

Accepted

### Context

Camera streaming requires long-lived connections. Vercel serverless functions are not designed for long-running camera proxy streams.

### Decision

Use Vercel for dashboard/API only. Use a home gateway and tunnel for stream access.

### Consequences

- More stable.
- Requires a PC, notebook, Raspberry Pi, or mini PC for remote stream.
- Cloudflare Tunnel or ngrok can be used later.
