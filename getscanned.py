import asyncio
import aiohttp
import subprocess
import time
import requests
import urllib.parse
import sys
from datetime import datetime, timezone

ZAP_CONTAINER_NAME = "dualhook_zap"
ZAP_API_URL = "http://localhost:8080"

async def send_to_webhook(webhook_url, payload):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(webhook_url, json=payload) as response:
                if response.status != 204:
                    print(f"Webhook status: {response.status}")
    except Exception as e:
        print(f"Webhook failed: {str(e)}")

def print_progress(phase, current, total=100):
    bar_length = 30
    filled = int(bar_length * current / total)
    bar = '█' * filled + '░' * (bar_length - filled)
    print(f"\r{phase}: |{bar}| {current}%", end="")
    if current >= total:
        print("\n")

def start_zap():
    print("Starting fresh OWASP ZAP instance...")
    subprocess.run(["docker", "rm", "-f", ZAP_CONTAINER_NAME], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    subprocess.Popen([
        "docker", "run", "-d",
        "--name", ZAP_CONTAINER_NAME,
        "-p", "8080:8080",
        "zaproxy/zap-stable",
        "zap.sh", "-daemon",
        "-host", "0.0.0.0", "-port", "8080",
        "-config", "api.disablekey=true",
        "-config", "api.addrs.addr.name=.*",
        "-config", "api.addrs.addr.regex=true"
    ])

    print("Waiting for ZAP to boot and API to be ready...")
    zap_version = "Unknown"
    for i in range(1, 71):
        print_progress("Booting ZAP", min(i, 70), 70)
        time.sleep(1)
        try:
            resp = requests.get(f"{ZAP_API_URL}/JSON/core/view/version/", timeout=5)
            if resp.status_code == 200:
                zap_version = resp.json()["version"]
                print(f"\nZAP {zap_version} is ready!")
                time.sleep(5)
                return zap_version
        except:
            continue
    print("\nWarning: ZAP boot timeout – continuing")
    return zap_version

def stop_zap():
    print("Cleaning up ZAP container...")
    subprocess.run(["docker", "rm", "-f", ZAP_CONTAINER_NAME], stdout=subprocess.DEVNULL)

def run_zap_scan(target_url):
    encoded = urllib.parse.quote(target_url, safe='')
    print(f"\nSpidering target: {target_url}")

    requests.get(
        f"{ZAP_API_URL}/JSON/spider/action/scan/",
        params={
            "url": target_url,
            "maxChildren": "20",
            "recurse": "true"
        },
        timeout=10
    )

    spider_progress = 0
    for _ in range(50):
        try:
            status_resp = requests.get(f"{ZAP_API_URL}/JSON/spider/view/status/", timeout=5)
            if status_resp.status_code == 200:
                spider_progress = int(status_resp.json()["status"])
                print_progress("Spidering", spider_progress)
                if spider_progress >= 100:
                    break
        except:
            print_progress("Spidering", spider_progress)
        time.sleep(3)

    print("\nRunning passive + baseline scan...")
    time.sleep(8)

    alerts_resp = requests.get(
        f"{ZAP_API_URL}/JSON/core/view/alerts/",
        params={"baseurl": target_url},
        timeout=10
    )
    alerts = alerts_resp.json()["alerts"] if alerts_resp.status_code == 200 else []

    high = [a for a in alerts if a["risk"] == "High"]
    medium = [a for a in alerts if a["risk"] == "Medium"]
    low = [a for a in alerts if a["risk"] == "Low"]
    info = [a for a in alerts if a["risk"] == "Informational"]

    return {
        "high": len(high),
        "medium": len(medium),
        "low": len(low),
        "info": len(info),
        "top_alerts": (high + medium + low)[:15]
    }

async def main(target_url, webhook_summary, webhook_details):
    if not target_url.startswith(("http://", "https://")):
        print("Error: URL must start with http:// or https://")
        return

    scan_start_time = datetime.now(timezone.utc)
    print(f"Scan started at: {scan_start_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")

    zap_version = start_zap()
    try:
        results = run_zap_scan(target_url)
        scan_end_time = datetime.now(timezone.utc)
        duration = scan_end_time - scan_start_time
        duration_str = str(duration).split('.')[0]  

        color = 16711680 if results["high"] > 0 else (16580616 if results["medium"] > 0 else 65280)
        timestamp = scan_end_time.isoformat()

        
        summary_embed = {
            "title": "Scan Report",
            "description": f"**Target:** `{target_url}`\n**Completed:** {scan_end_time.strftime('%H:%M UTC')} • **Duration:** `{duration_str}`",
            "color": color,
            "fields": [
                {"name": "Risk Summary", "value": f"🔴 **{results['high']}** 🟠 **{results['medium']}** 🟡 {results['low']} ℹ️ {results['info']}", "inline": False},
                {"name": "Total Alerts", "value": f"**{results['high'] + results['medium'] + results['low'] + results['info']}**", "inline": True},
                {"name": "Risk Level", "value": "Critical 🔴" if results["high"] > 0 else ("Elevated 🟠" if results["medium"] > 0 else "Secure 🟢"), "inline": True},
                {"name": "ZAP Version", "value": zap_version, "inline": True}
            ],
            "author": {
                "name": "saint-sql",
                "icon_url": "https://avatars.githubusercontent.com/u/231521105?s=400&u=7a1e25fdf7a1b5e1b4872ada8b595a9d859c0f26&v=4"
            },
            "footer": {
                "text": "Made by saint-sql • United Kingdom • CyberSec @ 20",
                "icon_url": "https://www.freeiconspng.com/thumbs/heart-icon/heart-outline-19.png"  
            },
            "timestamp": timestamp
        }

        
        detail_fields = []
        for alert in results["top_alerts"]:
            emoji = {"High": "🔴", "Medium": "🟠", "Low": "🟡", "Informational": "ℹ️"}.get(alert["risk"], "❓")
            detail_fields.append({
                "name": f"{emoji} {alert['alert']} ({alert['risk']})",
                "value": f"{alert['description'][:240]}...\n**Location:** {alert.get('url', 'Multiple')}",
                "inline": False
            })

        if not detail_fields:
            detail_fields.append({"name": "No Vulnerabilities Detected", "value": "Excellent security"})

        details_embed = {
            "title": f"📋 Detailed Findings — {target_url}",
            "description": f"Top {len(detail_fields)} alerts from OWASP ZAP scan",
            "color": color,
            "fields": detail_fields,
            "footer": {
                "text": "DualHook-Scan • Scanned by saint-sql 🇬🇧"
            },
            "timestamp": timestamp
        }

        await asyncio.gather(
            send_to_webhook(webhook_summary, {"embeds": [summary_embed]}),
            send_to_webhook(webhook_details, {"embeds": [details_embed]})
        )
        print(f"\nScan completed in {duration_str}! Alerts sent to Discord")

    finally:
        stop_zap()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("\nUsage: python getscanned.py <target_url> <summary_webhook> <details_webhook>")
        print("Example: python getscanned.py https://scanme.nmap.org webhook1 webhook2\n")
        sys.exit(1)
    
    asyncio.run(main(sys.argv[1], sys.argv[2], sys.argv[3]))