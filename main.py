import requests
import time

TELEGRAM_TOKEN = "8786606551:AAGTwTWZoMvnncy3Gw2M22bJb_XsA2mF1Ys"
CHAT_ID = "7256257117"

def send_telegram(message, photo_url=None):
    if photo_url:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
        requests.post(url, data={"chat_id": CHAT_ID, "photo": photo_url, "caption": message})
    else:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": message})

def search_vinted(query):
    url = "https://www.vinted.fr/api/v2/catalog/items"
    params = {"search_text": query, "per_page": 5, "order": "newest_first"}
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, params=params, headers=headers)
        return r.json().get("items", [])
    except:
        return []

seen = set()

def check(query):
    items = search_vinted(query)
    for item in items:
        if item["id"] not in seen:
            seen.add(item["id"])
            msg = f"🛍 {item['title']}\n💶 {item['price']} €\n📏 {item.get('size_title','?')}\n⭐ {item.get('status','?')}\n🔗 https://www.vinted.fr{item['path']}"
            send_telegram(msg, item.get("photo", {}).get("url"))

QUERY = "Ralph Lauren pantalon"

print("Bot démarré !")
send_telegram(f"✅ Bot lancé ! Surveillance de : {QUERY}")

while True:
    check(QUERY)
    time.sleep(30)
