import requests
import json

TELEGRAM_TOKEN = "8786606551:AAGU4vH5rMYhGCv_oucmvSjmdzhnTLtT58g"
CHAT_ID = "7256257117"
QUERY = "nike running phenom elite tech"
SEEN_FILE = "seen.json"

def load_seen():
    try:
        with open(SEEN_FILE) as f:
            return set(json.load(f))
    except:
        return set()

def save_seen(seen):
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen), f)

def send_telegram(message, photo_url=None):
    if photo_url:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
        requests.post(url, data={"chat_id": CHAT_ID, "photo": photo_url, "caption": message})
    else:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": message})

def search_vinted(query):
    url = "https://www.vinted.fr/api/v2/catalog/items"
    params = {
        "search_text": query,
        "per_page": 20,
        "order": "newest_first",
        "size_ids": "1"
    }
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, params=params, headers=headers)
        return r.json().get("items", [])
    except:
        return []

seen = load_seen()
items = search_vinted(QUERY)
for item in items:
    if str(item["id"]) not in seen:
        seen.add(str(item["id"]))
        msg = f"🛍 {item['title']}\n💶 {item['price']} €\n📏 {item.get('size_title','?')}\n⭐ {item.get('status','?')}\n🔗 https://www.vinted.fr{item['path']}"
        send_telegram(msg, item.get("photo", {}).get("url"))

save_seen(seen)
