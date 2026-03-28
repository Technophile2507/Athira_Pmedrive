import requests
import time
import os

# --- Configuration ---
# Use environment variables for security on Render
TOKEN = "8781936268:AAFrpBDaptH6sLlJUWG1Tb5SgdOZGSnPhYg"
CHAT_ID = 441414836
# The actual site you want to monitor
TARGET_URL = "https://pmedrive.heavyindustries.gov.in" 
INTERVAL = 60  # seconds

def send_telegram_msg(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error sending Telegram message: {e}")

def check_site():
    print(f"Checking {TARGET_URL}...")
    try:
        # We check the actual gov.in site, not the 'isitdown' info page
        response = requests.get(TARGET_URL, timeout=10)
        if response.status_code == 200:
            return True
        else:
            return False
    except:
        return False

def main():
    last_status = None # Keep track of previous state
    
    print("Monitor started...")
    send_telegram_msg("🚀 Website Monitor started for PMEDrive.")

    while True:
        is_up = check_site()
        
        # Logic: Notify only if the status CHANGED to 'UP'
        if is_up and last_status is False:
            send_telegram_msg(f"✅ ALERT: {TARGET_URL} is now UP!")
        elif not is_up and (last_status is True or last_status is None):
            print("Site is currently down.") 
            # Optional: Notify when it goes DOWN
            # send_telegram_msg(f"❌ ALERT: {TARGET_URL} is DOWN!")

        last_status = is_up
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
