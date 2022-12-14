from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import datetime
import pandas as pd


#  뉴스 기사와 기자는 저작물로 등록되어있기 때문에 별도의 상업적인 용도로 사용은 불가

# 시간 변수 선언
today = datetime.datetime.now().date()
yesterday = today - datetime.timedelta(1)

full_report = {}

# 빅카인즈 홈페이지 띄우기
wd = webdriver.Chrome()
wd.implicitly_wait(3)  # 3초간 반복적으로 작업이 수행될 때까지 반복하는 것
url = r'https://www.bigkinds.or.kr'
wd.get(url)
time.sleep(1)

news_search = wd.find_element(By.XPATH, '/html/body/div[1]/header/div[1]/div/form/div/div[1]/div[1]/input[1]')
news_search.send_keys("좀비")  # 보유 중인 주식명 기입
# time.sleep()
detail_search = wd.find_element(By.XPATH, '/html/body/div[1]/header/div[1]/div/form/div/div[1]/button')
detail_search.click()    # 상세검색 버튼 클릭
time.sleep(1)
seoul_check = wd.find_element(By.XPATH, '/html/body/div[1]/header/div[1]/div/form/div/div[1]/div[2]/div/div[1]/div[4]/div[1]/span[1]/label')
seoul_check.click()   # 언론사 서울 지정
#time.sleep(1)
period = wd.find_element(By.XPATH, '/html/body/div[1]/header/div[1]/div/form/div/div[1]/div[2]/div/div[1]/div[1]/a')
period.click()   # 기간 선택
time.sleep(1)
period_start = wd.find_element(By.XPATH, '/html/body/div[1]/header/div[1]/div/form/div/div[1]/div[2]/div/div[1]/div[2]/div/div[2]/div/div[1]/input')
for _ in range(10):
    period_start.send_keys(Keys.BACK_SPACE)  # 기존 입력값 삭제
#time.sleep(1)
period_start.send_keys(f'{yesterday}')   # 하루전 날짜 입력
#time.sleep(1)
apply_option = wd.find_element(By.XPATH, '/html/body/div[1]/header/div[1]/div/form/div/div[1]/div[2]/div/div[4]/div[2]/button[2]')
apply_option.click()  # 기간, 언론사 세부검색 적용
time.sleep(1)

n = int(wd.find_element(By.XPATH, '/html/body/div[1]/main/div[1]/div[2]/div/div[2]/div[2]/div/div[2]/div[3]/div[3]/h3/span[6]').text) // 10 + 1  # 페이지 수
time.sleep(1)
m = int(wd.find_element(By.XPATH, '/html/body/div[1]/main/div[1]/div[2]/div/div[2]/div[2]/div/div[2]/div[3]/div[3]/h3/span[6]').text) % 10  # 마지막 페이지 기사 개수
time.sleep(1)

for pg in range(1, n + 1):  # 전체 페이지 수 만큼 반복
    if n == 1 and m == 0:  # 기사가 0개
        break
    if (n == 1 and m != 0) or pg == n:  # 기사 10개 미만이거나 마지막 페이지 일 때
        for a in range(1, m + 1):
            wd.find_element(By.XPATH, f'/html/body/div[1]/main/div[1]/div[2]/div/div[2]/div[2]/div/div[2]/div[3]/div[5]/div[{a}]/div/div[2]/a/div/strong/span').click()  # 기사제목 클릭
            time.sleep(1)
            title = wd.find_element(By.XPATH, '/html/body/div[4]/div/div/div[1]/div/div[1]/h1').text
            report = wd.find_element(By.XPATH, '/html/body/div[4]/div/div/div[1]/div/div[2]').text.replace('\n', ' ')
            time.sleep(2)
            full_report[title] = report    # 기사 제목별 본문내용 매치, 딕셔너리 저장
            wd.find_element(By.XPATH,'/html/body/div[4]/div/div/button').click()  # 기사창 닫기 버튼 클릭
            time.sleep(1)
    else:   # 마지막 페이지가 아닐 때
        for b in range(1, 11):  # 기사 1 ~ 10번
            wd.find_element(By.XPATH, f'/html/body/div[1]/main/div[1]/div[2]/div/div[2]/div[2]/div/div[2]/div[3]/div[5]/div[{b}]/div/div[2]/a/div/strong/span').click()  # 기사제목 클릭
            time.sleep(1)
            title = wd.find_element(By.XPATH, '/html/body/div[4]/div/div/div[1]/div/div[1]/h1').text
            report = wd.find_element(By.XPATH, '/html/body/div[4]/div/div/div[1]/div/div[2]').text.replace('\n', ' ')
            time.sleep(2)
            full_report[title] = report    # 기사 제목별 본문내용 매치, 딕셔너리 저장
            wd.find_element(By.XPATH,'/html/body/div[4]/div/div/button').click()  # 기사창 닫기 버튼 클릭
            time.sleep(1)
        wd.find_element(By.XPATH, '/html/body/div[1]/main/div[1]/div[2]/div/div[2]/div[2]/div/div[2]/div[3]/div[7]/div[1]/div/div/div/div[4]/a').click()  # 다음 페이지로 이동
    time.sleep(1)

print(full_report)  # 리포트 제목: 본문 형태로 여러개가 저장된 딕셔너리..

# 최종 파일 저장
df = pd.DataFrame({'news title': full_report.keys(), 'content': full_report.values()})
df.to_csv('news_main.csv', index=False,  encoding='cp949')
