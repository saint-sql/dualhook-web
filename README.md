<p align="center">
  <img src="https://avatars.githubusercontent.com/u/231521105?s=400&u=7a1e25fdf7a1b5e1b4872ada8b595a9d859c0f26&v=4" width="180" alt="Profile Picture"/>
</p>

<h1 align="center">DualHook-Web 🛡️</h1>

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

- Real **OWASP ZAP Baseline Scan** (passive + light active) via Docker
- Fast scans (~1-2 minutes)
- Compact summary + detailed findings in Discord
- Terminal progress bars
- Professional Discord embeds with risk levels and timestamps

## Prerequisites

**Docker Desktop is required** (OWASP ZAP runs in a container).

1. Download & install:  
   [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)

2. Start Docker Desktop and wait for **"Docker is running"**.

3. Verify:
   ```bash
   docker --version
   docker run hello-world
