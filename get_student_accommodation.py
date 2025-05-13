from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import os, time, requests, re

# Load environment variables from .env file
load_dotenv()

TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH", "/usr/local/bin/chromedriver")

URL = os.getenv("CHECK_URL", 'https://www.studentbostader.se/en/find-apartments/search-apartments/?sortering=hyra')

RENT_PRICE = int(os.getenv("PRICE_LIMIT", 8000))

# Function to send a message to Telegram
def send_telegram_message(message):
    api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    response = requests.post(api_url, data=data)
    return response.json().get("ok", False)

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

        # If there are available listings, check the price
        if value > 0:
            # Count the number of listings with a price less than RENT_PRICE kr.
            price_elements = driver.find_elements(By.CSS_SELECTOR, "div.ObjektHyra")
            affordable_count = 0
            for el in price_elements:
                price_text = el.text
                cleaned = re.sub(r"[^\d]", "", price_text)
                if cleaned.isdigit():
                    price = int(cleaned)
                    if price < RENT_PRICE:
                        affordable_count += 1

            print("Affordable (<", RENT_PRICE,"kr) listings:", affordable_count)
            if affordable_count > 0:
                print("Affordable listings found, sending notification.")
                # Send a message to Telegram
                message = f"{value} are available now!\n {affordable_count} are affordable (<{RENT_PRICE}kr) listings.\n{URL}"
                if send_telegram_message(message):
                    print("Notification sent to Telegram.")

        driver.quit()

    except Exception as e:
        print("An error occurred:", e)

    time.sleep(120)
