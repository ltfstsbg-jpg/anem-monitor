import requests
import os

CARD_NUMBER = os.environ.get("CARD_NUMBER")
NIN_OR_ID   = os.environ.get("NIN_OR_ID")
BOT_TOKEN   = os.environ.get("BOT_TOKEN")
CHAT_ID     = os.environ.get("CHAT_ID")

NO_APPT_TEXTS = ["aucun rendez-vous", "pas de rendez-vous", "لا يوجد موعد"]

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": message})

def check_appointment():
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://minha.anem.dz/",
        "Origin": "https://minha.anem.dz",
    })

    try:
        login_url = "https://minha.anem.dz/api/pre-inscription/login"
        payload = {
            "numeroWassit": CARD_NUMBER,
            "numeroPieceIdentite": NIN_OR_ID
        }
        r = session.post(login_url, json=payload, timeout=30)
        print(f"Login status: {r.status_code}")
        print(f"Login response: {r.text[:500]}")

        if r.status_code != 200:
            print("فشل تسجيل الدخول")
            return False

        rdv_url = "https://minha.anem.dz/api/pre-inscription/rendez-vous"
        r2 = session.get(rdv_url, timeout=30)
        print(f"RDV status: {r2.status_code}")
        print(f"RDV response: {r2.text[:500]}")

        page_text = r2.text.lower()
        for txt in NO_APPT_TEXTS:
            if txt.lower() in page_text:
                print("لا يوجد موعد حالياً.")
                return False

        print("يوجد موعد!")
        return True

    except Exception as e:
        print(f"خطأ: {e}")
        return False

print("جاري الفحص...")
found = check_appointment()
if found:
    send_telegram("✅ تم العثور على موعد! سارع للتسجيل الآن!\nhttps://minha.anem.dz/pre_inscription")
    print("تم إرسال إشعار Telegram!")
else:
    print("لا يوجد موعد حالياً.")
