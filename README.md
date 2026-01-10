<p align="center">
  <img src="https://avatars.githubusercontent.com/u/231521105?s=400&u=7a1e25fdf7a1b5e1b4872ada8b595a9d859c0f26&v=4" width="180" alt="Profile Picture"/>
</p>

<h1 align="center">DualHook</h1>

<p align="center">
  <strong>Web Vulnerability Scanner</strong><br>
  Powered by OWASP ZAP Baseline Scan • Dual Discord Webhook Alerts
</p>

<p align="center">
  <a href="https://github.com/saint-sql/dualhook-web/stargazers">
    <img alt="GitHub stars" src="https://img.shields.io/github/stars/saint-sql/dualhook-web?style=social">
  </a>
  <a href="https://github.com/saint-sql/dualhook-web/forks">
    <img alt="GitHub forks" src="https://img.shields.io/github/forks/saint-sql/dualhook-web?style=social">
  </a>
</p>

<p align="center">
  Made by <strong>saint-sql</strong> 🇬🇧 | 20 | CyberSec Enthusiast
</p>

---

## Features

- **OWASP ZAP Baseline Scan** (passive scan) via Docker
  + Also has a passive spider scan ran in background
- Swift Scan
- Compact summary + scans attached to webhook via discord integration 
- Terminal progress
- Discord embeds with risk levels and timestamps

## Prerequisites

**Docker Desktop is required** (OWASP ZAP runs in a container).

1. Download & install:  
   [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)

2. Start Docker Desktop and wait for **"Docker is running"**.

3. Verify:
   ```bash
   docker --version
   docker run hello-world
   
## Installation
 ```bash
git clone https://github.com/saint-sql/dualhook-web.git
cd dualhook-web
pip install -r requirements.txt
```
## Setting Up Discord Webhooks

In your Discord server: Server Settings → Integrations → Webhooks → Create Webhook
Create two webhooks (preferably in separate channels):
One for summary (quick overview)
One for detailed findings

Copy each webhook URL (e.g., https://discord.com/api/webhooks/...)

## Usage
```Run a scan:
python getscanned.py <target_url> <summary_webhook_url> <details_webhook_url>
```
```
python getscanned.py https://scanme.nmap.org https://discord.com/api/webhooks/.../summary https://discord.com/api/webhooks/.../details
```
## Recommended test targets:

https://scanme.nmap.org (official ZAP testing site)

https://httpbin.org (fast & clean)

## Disclaimer
Educational and ethical use only.
Only scan sites you own or have explicit permission to test.
No responsibility for misuse. I dont
fancy jailtime for your silly decisions
