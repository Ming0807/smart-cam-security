# Skill: Cloudflare Tunnel and Remote Access

## Use This Skill When

Working on optional remote stream access.

## Important Rule

ESP32-CAM does not run Cloudflare Tunnel directly.

A home gateway must run the tunnel:

- PC
- Notebook
- Raspberry Pi
- Mini PC

## Options

### Cloudflare Quick Tunnel

Good for testing. No custom domain needed. URL may change.

### Cloudflare Tunnel with Custom Domain

Best for production. Requires a domain.

### ngrok Free Dev Domain

Good alternative when no custom domain is available.

## Do Not

- Proxy long-running camera stream through Vercel.
- Expose unnecessary local services.
