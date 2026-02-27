#!/usr/bin/env python3
# ping.py - Ping Service for OSINT Bot (keeps main bot awake)

import os
import time
import threading
import requests
from flask import Flask

app = Flask(__name__)

# ==================== CONFIGURATION ====================
# अपने मुख्य बॉट का URL यहाँ डालें (Render का असली URL)
TARGET_URL = "https://osint-bot1.onrender.com/health"  # इसे बदलें
PING_INTERVAL = 300  # 5 मिनट (सेकंड में)

# ==================== PING FUNCTION ====================
def ping_bot():
    """हर PING_INTERVAL सेकंड में TARGET_URL को पिंग करता है"""
    while True:
        try:
            response = requests.get(TARGET_URL, timeout=10)
            print(f"✅ Pinged {TARGET_URL} - Status: {response.status_code}")
        except Exception as e:
            print(f"❌ Ping failed: {e}")
        time.sleep(PING_INTERVAL)

# ==================== FLASK ROUTES ====================
@app.route('/')
def home():
    """UptimeRobot या अन्य सर्विस इस एंडपॉइंट को पिंग करेगी"""
    return "Ping Service is running. Main bot is being kept alive."

@app.route('/health')
def health():
    """हेल्थ चेक के लिए"""
    return {"status": "alive", "target": TARGET_URL}

# ==================== MAIN ====================
if __name__ == "__main__":
    # पिंग थ्रेड स्टार्ट करें (daemon=True ताकि Flask बंद होने पर यह भी बंद हो जाए)
    thread = threading.Thread(target=ping_bot, daemon=True)
    thread.start()
    
    # Flask सर्वर चलाएँ (Render पर PORT एनवायरनमेंट वेरिएबल से मिलता है)
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Ping Service started on port {port}")
    app.run(host="0.0.0.0", port=port)
