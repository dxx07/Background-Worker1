
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import requests

# --- CONFIG ---
TELEGRAM_BOT_TOKEN = '6707955546:AAExPQfo2O4qV3-L-z2s0oWpTyXhQJDd-_w'
TELEGRAM_CHAT_ID = '1025862582'
CHECK_URL = "https://prenotami.esteri.it/Services"  # Replace with correct visa booking URL
CHECK_INTERVAL = 600  # seconds

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
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(CHECK_URL)
        time.sleep(5)  # wait for page to load

        if "non ci sono date disponibili" in driver.page_source.lower() or            "sorry, all appointments for this service are currently booked" in driver.page_source.lower():
            print("❌ No available dates.")
        else:
            print("✅ Slot might be available!")
            send_telegram_message("✅ Italian visa slot might be available! Check: " + CHECK_URL)
    except Exception as e:
        print("Error checking site:", e)
    finally:
        driver.quit()

if __name__ == "__main__":
    while True:
        check_slot()
        time.sleep(CHECK_INTERVAL)
