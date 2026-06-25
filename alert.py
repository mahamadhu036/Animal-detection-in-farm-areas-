import requests
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID


def send_telegram(animal, timestamp):
    """Send Telegram alert when an animal is detected."""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        response = requests.post(url, data={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": (
                f"🚨 Farm Alert!\n"
                f"🐾 Animal: {animal.upper()}\n"
                f"🕐 Time: {timestamp}"
            )
        })
        result = response.json()
        if result.get("ok"):
            print("✅ Telegram alert sent!")
        else:
            print(f"⚠️  Telegram warning: {result.get('description')}")
    except Exception as e:
        print(f"❌ Telegram error: {e}")


def send_all_alerts(animal, timestamp, img_path):
    """Send all configured alerts (currently Telegram only)."""
    send_telegram(animal, timestamp)