
import time
import requests

# --- CONFIG ---
TELEGRAM_BOT_TOKEN = '6707955546:AAExPQfo2O4qV3-L-z2s0oWpTyXhQJDd-_w'
TELEGRAM_CHAT_ID = '1025862582'
CHECK_URL = "https://prenotami.esteri.it/Services/Booking/5"
CHECK_INTERVAL = 600  # 10 минут

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    try:
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            print("Failed to send message:", response.text)
    except Exception as e:
        print("Telegram error:", e)

def check_slot():
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(CHECK_URL, headers=headers)
        if response.status_code != 200:
            print("Website error:", response.status_code)
            return

        content = response.text.lower()
        if "non ci sono date disponibili" in content or "sorry, all appointments for this service are currently booked" in content:
            print("❌ No available dates.")
        else:
            print("✅ Slot might be available!")
            send_telegram_message("✅ Italian visa slot might be available! Check: " + CHECK_URL)
    except Exception as e:
        print("Error checking site:", e)

if __name__ == "__main__":
    while True:
        check_slot()
        time.sleep(CHECK_INTERVAL)
