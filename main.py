import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import requests

TOKEN = os.environ.get("TELEGRAM_TOKEN", "여기에_토큰_넣기")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "여기에아이디_넣기")
OPEN_CHAT_URL = "https://open.kakao.com/o/sGAHKZli"

CLOSED_WORDS = [
    "참여하실 수 없습니다", "인원이 제한", "만료된",
    "참여코드", "정원이 마감", "마감되었습니다",
]

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": text}, timeout=10)
    except Exception as e:
        print("텔레그램 발송 오류:", e)

def make_driver():
    options = Options()
    options.binary_location = "/usr/bin/chromium"   # 서버에 설치된 크롬 위치
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    service = Service("/usr/bin/chromedriver")      # 서버에 설치된 드라이버 위치
    return webdriver.Chrome(service=service, options=options)

def check_open_chat():
    print("🕵️ 감시 시작! (60초 간격)")
    send_telegram_message("🚀 감시 봇이 출동했어!")

    while True:
        driver = None
        try:
            driver = make_driver()
            driver.get(OPEN_CHAT_URL)
            time.sleep(3)

            page_text = driver.find_element(By.TAG_NAME, "body").text
            print("📄 페이지 내용:", page_text[:200].replace("\n", " | "))

            # 페이지가 비어있으면 접속 실패(차단 등)라서 알림 안 보냄
            if len(page_text.strip()) < 5:
                print("⚠️ 페이지가 비어있어. 차단됐을 수 있어!")
            elif any(w in page_text for w in CLOSED_WORDS):
                print("🔒 아직 마감 상태... 💤")
            else:
                print("🔓 마감 문구가 사라졌어!!!")
                send_telegram_message(
                    f"🚨 오픈채팅 마감 문구가 사라졌어!! 당장 확인해봐!!\n👉 {OPEN_CHAT_URL}"
                )
                time.sleep(600)

        except Exception as e:
            print("오류 발생 (다시 시도합니다):", e)
        finally:
            if driver:
                driver.quit()

        time.sleep(60)

if __name__ == "__main__":
    check_open_chat()
