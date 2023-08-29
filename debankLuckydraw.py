from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import csv
import re

# ตั้งค่า WebDriver
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument('--profile-directory=Profile 1')
options.add_argument('--user-data-dir=C:\\Users\\kemma\\AppData\\Local\\Google\\Chrome\\User Data\\')
driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))

# เปิดเว็บและตรวจสอบ element พร้อมบันทึกข้อมูล
def process_link(stream_id, csv_writer):
    url = f"https://debank.com/stream/{stream_id}"
    driver.get(url)

    try:
        wait = WebDriverWait(driver, 2)  # รอเวลาไม่เกิน 5 วินาที

        latest_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[1]/div/div[2]/div[1]/div[3]/div/div[2]/div/button'))) # ปุ่ม Latest
        latest_button.click()

        prize_name_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[1]/div/div[2]/div[1]/div[3]/div/div[2]/div/div[2]/span[1]')))
        prize_name = prize_name_element.text
        prize_count_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[1]/div/div[2]/div[1]/div[3]/div/div[2]/div/div[2]/span[2]')))
        prize_count = prize_count_element.text
        participants_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[1]/div/div[2]/div[1]/div[3]/div/div[3]/div/span')))
        participants = participants_element.text
        
        # ใช้ regex เพื่อเอาเฉพาะตัวเลข
        prize_name = int(re.search(r'\d+', prize_name).group())
        prize_count = int(re.search(r'\d+', prize_count).group())
        participants = int(re.search(r'\d+', participants).group())

        chance = (prize_count / participants) * 100
        
        csv_writer.writerow([url, prize_name, prize_count, participants, chance])
        print(f"Data found for {url}")
    except:
        print(f"Data not found for {url}")

# รันโปรแกรม
try:
    with open('data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['URL', 'Prize Name', 'Prize Count', 'Participants', 'Percent'])

        start_id = 524931
        current_id = start_id

        while True:
            process_link(current_id, csv_writer)
            current_id += 1
except KeyboardInterrupt:
    print(f"Stopped at ID: {current_id}")

# ปิดเบราว์เซอร์
driver.quit()
