from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os, time, requests, json

TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH", "/usr/local/bin/chromedriver")

URL = os.getenv("CHECK_URL")

while True:
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        service = webdriver.chrome.service.Service(CHROMEDRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=chrome_options)

        driver.get(URL)

        element = driver.find_element(By.CSS_SELECTOR, 'strong')
        value = int(element.text)
        print("Offers available:", value)

        if value > 0:
            message = f"{value} 个房源现在可用！"
            api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
            response = requests.post(api_url, data=data)

            if response.json().get("ok"):
                print("Notification sent to Telegram.")

        driver.quit()

    except Exception as e:
        print("An error occurred:", e)

    time.sleep(180)
