import os
import time
import requests
import threading
from flask import Flask

app = Flask(__name__)

# --- Configuration ---
TOKEN = "8781936268:AAFrpBDaptH6sLlJUWG1Tb5SgdOZGSnPhYg"
CHAT_ID = 441414836
TARGET_URL = "https://pmedrive.heavyindustries.gov.in"
INTERVAL = 60 

def send_telegram_msg(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": message})
    except Exception as e:
        print(f"Telegram Error: {e}")

def monitor_logic():
    last_status = None
    print("Monitoring thread started...")
    while True:
        try:
            # Checking the site status
            response = requests.get(TARGET_URL, timeout=10)
            is_up = (response.status_code == 200)
            
            # Notify on status change (Down -> Up)
            if is_up and last_status is False:
                send_telegram_msg(f"✅ ALERT: {TARGET_URL} is now UP!")
            elif not is_up and (last_status is True or last_status is None):
                print(f"Site is down (Status: {response.status_code})")
            
            last_status = is_up
        except Exception as e:
            print(f"Check Error: {e}")
            last_status = False
            
        time.sleep(INTERVAL)

@app.route('/')
def home():
    return "Monitor is running!", 200

if __name__ == "__main__":
    # Start the monitoring loop in a separate thread
    threading.Thread(target=monitor_logic, daemon=True).start()
    # Start the Flask web server
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
