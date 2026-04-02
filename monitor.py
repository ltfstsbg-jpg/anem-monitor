import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

CARD_NUMBER = "400298014600"
NIN_OR_ID   = "109980090014600005"
BOT_TOKEN   = "8673770315:AAHEeYs2xBq95rXnReIrz-_z6W9H49GRxYo"
CHAT_ID     = "5492379451"
CHECK_INTERVAL = 1800

def send_telegram(message):
    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": message},
            timeout=10
        )
    except:
        pass

def check_appointment():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280,800")
    options.binary_location = "/data/data/com.termux/files/usr/bin/chromium-browser"

service = Service("/data/data/com.termux/files/usr/bin/chromedriver", service_args=["--timeout=120"])
driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 40)

    try:
        print("opening site...")
        driver.get("https://minha.anem.dz/pre_inscription")

        field1 = wait.until(EC.presence_of_element_located((By.ID, "numeroWassit")))
        field1.clear()
        field1.send_keys(CARD_NUMBER)

        field2 = wait.until(EC.presence_of_element_located((By.ID, "numeroPieceIdentite")))
        field2.clear()
        field2.send_keys(NIN_OR_ID)

        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        submit.click()
        print("submitted, waiting...")
        time.sleep(5)

        try:
            cont = WebDriverWait(driver, 6).until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(),'Continuer') or contains(text(),'Suivant')]")
            ))
            cont.click()
            print("clicked continuer")
            time.sleep(4)
        except:
            print("no continuer button")

        page = driver.page_source.lower()
        print("page snippet:", page[1000:1200])

        if "aucun rendez-vous" in page or "noacun" in page or "pas de rendez" in page:
            print("no appointment")
            return False

        print("APPOINTMENT FOUND!")
        return True

    except Exception as e:
        print("error:", e)
        return False
    finally:
        driver.quit()

print("started monitoring...")
send_telegram("started monitoring - will notify when appointment is available")

while True:
    try:
        found = check_appointment()
        if found:
            send_telegram("APPOINTMENT FOUND!\nhttps://minha.anem.dz/pre_inscription")
    except Exception as e:
        print("general error:", e)
    time.sleep(CHECK_INTERVAL)
