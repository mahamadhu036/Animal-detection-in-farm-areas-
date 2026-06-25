import requests
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

print("Testing Telegram Alert...")
print("-" * 40)

url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

try:
    response = requests.post(url, data={
        "chat_id": TELEGRAM_CHAT_ID,
        "text": "✅ Telegram Test Message!\n🐾 Alert system working!"
    })
    
    result = response.json()
    
    if result['ok']:
        print("✅ SUCCESS! Message sent to Telegram!")
        print(f"Message ID: {result['result']['message_id']}")
    else:
        print("❌ FAILED! Check your token and chat ID")
        print(result)
        
except Exception as e:
    print(f"❌ ERROR: {e}")

print("-" * 40)