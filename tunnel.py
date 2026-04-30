"""
Run this script to start Flask + ngrok tunnel.
Your app will be accessible from anywhere via a public URL.

Usage:
    python tunnel.py
"""

from pyngrok import ngrok, conf, process
import subprocess
import sys
import time

# ── PASTE YOUR NGROK AUTH TOKEN HERE ────────────────────────
NGROK_AUTH_TOKEN = "PASTE_YOUR_TOKEN_HERE"
# ────────────────────────────────────────────────────────────

if NGROK_AUTH_TOKEN == "PASTE_YOUR_TOKEN_HERE":
    print("\n[!] Please open tunnel.py and paste your ngrok auth token.")
    print("    Get it free at: https://ngrok.com\n")
    sys.exit(1)

# Kill any existing ngrok processes cleanly
try:
    ngrok.kill()
    time.sleep(1)
except Exception:
    pass

# Set auth token
conf.get_default().auth_token = NGROK_AUTH_TOKEN

# Start Flask in background
print("[*] Starting Flask app...")
flask_proc = subprocess.Popen(
    [sys.executable, "app.py"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)
time.sleep(2)  # Wait for Flask to boot

# Open ngrok tunnel on port 5000
print("[*] Opening ngrok tunnel...")
try:
    tunnel = ngrok.connect(5000, "http")
    public_url = tunnel.public_url
except Exception:
    # If tunnel already exists, get it
    tunnels = ngrok.get_tunnels()
    if tunnels:
        public_url = tunnels[0].public_url
    else:
        print("[!] Could not create tunnel. Try again.")
        flask_proc.terminate()
        sys.exit(1)

print("\n" + "="*55)
print("  AI Email Intelligence System -- LIVE")
print("="*55)
print(f"  Public URL : {public_url}")
print(f"  Local URL  : http://127.0.0.1:5000")
print(f"  Admin Login: {public_url}/login")
print("="*55)
print("  Share the Public URL with anyone worldwide!")
print("  Press Ctrl+C to stop.\n")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n[*] Shutting down...")
    ngrok.kill()
    flask_proc.terminate()
    print("[*] Stopped. Goodbye!")

