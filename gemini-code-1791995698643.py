import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests

# ----------------- ⚠️ 여워의 정보 입력하는 곳 -----------------
# Railway 환경 변수(Variables)에 넣어두거나, 여기에 직접 적어줘도 돼!
TOKEN = os.environ.get("TELEGRAM_TOKEN", "여기에_토큰_넣기")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "여기에_숫자ID_넣기")
OPEN_CHAT_URL = "https://open.kakao.com/o/sGAHKZli"
# -------------------------------------------------------------

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print("텔레그램 발송 오류:", e)

def check_open_chat():
    # Railway 서버(리눅스) 환경에서 크롬이 안 튕기고 안전하게 돌도록 설정하는 옵션들이야!
    options = Options()
    options.add_argument("--headless")  # 화면 없는 서버니까 백그라운드 모드 필수!
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    
    print("🕵️ 물개 감시병 출동! 오픈채팅방 실시간 모니터링 시작... (60초 간격)")
    send_telegram_message("🚀 렐웨이 서버에서 오픈채팅 감시 봇이 출동했어, 여워야!")
    
    while True:
        driver = webdriver.Chrome(options=options)
        try:
            # 1. 오픈채팅 링크 접속
            driver.get(OPEN_CHAT_URL)
            time.sleep(3)
            
            # 2. 페이지 전체 텍스트 긁어오기
            page_text = driver.find_element(By.TAG_NAME, "body").text
            
            # 3. 마감 문구 감지
            is_closed = (
                "참여하실 수 없습니다" in page_text or 
                "인원이 제한" in page_text or 
                "만료된" in page_text or 
                "참여코드" in page_text or 
                "정원이 마감" in page_text or
                "마감되었습니다" in page_text
            )
            
            if is_closed:
                print("🔒 아직 마감 상태야... 조용히 대기 중 💤")
            else:
                print("🔓 대박!!! 마감 문구가 사라졌어격!!! 방 열렸다!!!")
                send_telegram_message(f"🚨 여워야!!! 오픈채팅 마감 문구가 사라졌어!! 진짜 열린 거 같아!! 당장 확인해봐!!\n👉 링크: {OPEN_CHAT_URL}")
                
                # 알림 보낸 후 10분 대기
                time.sleep(600)
                
        except Exception as e:
            print("오류 발생 (다시 시도합니다):", e)
            
        finally:
            driver.quit()
            
        time.sleep(60)

if __name__ == "__main__":
    check_open_chat()