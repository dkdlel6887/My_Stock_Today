# BeautifulSoup, Selenium 이용하여 Bigkinds 사이트에서 기사 긇어오기
# chrome version: 107.0.5304.107
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
#import requests
import time
from time import localtime
import pandas as pd
import datetime as dt

# Current_own.py에서 저장한 user_infos.xlsx에서 종목명만 불러와 리스트에 저장
stock_df = list(pd.read_excel('user_infos.xlsx', engine='openpyxl', header=0, index_col=0)['종목명'][:])

# 시간 변수 선언
now = dt.datetime.now().date()  # 오늘
yesterday = now - dt.timedelta(1)  # 전날


# 빅카인즈 홈페이지 띄우기
wd = webdriver.Chrome()
wd.implicitly_wait(3)  # 3초간 반복적으로 작업이 수행될 때까지 반복하는 것
url = r'https://www.bigkinds.or.kr/'
wd.get(url)
time.sleep(3)

titles = []   # 기사 제목 저장
urls = []  # 기사원본 링크 저장
# 주식 종목명 입력, 검색버튼 클릭, 관련기사 링크 종합하여 저장
for i in stock_df:  # stock 빈 리스트 형태로 불러옴, register_stock함수가 실행 되고난 뒤 불러올 수 있도록 해야함 or xlsx파일에서 불러오는걸로
    news_search = wd.find_element(By.XPATH, '/html/body/div[1]/header/div[1]/div/form/div/div[1]/div[1]/input[1]')
    news_search.send_keys(f"{i}")  # 보유 중인 주식명 기입
    time.sleep(3)
    detail_search = wd.find_element(By.XPATH, '/html/body/div[1]/header/div[1]/div/form/div/div[1]/button')
    detail_search.click()    # 상세검색 버튼 클릭
    time.sleep(3)
    seoul_check = wd.find_element(By.XPATH, '/html/body/div[1]/header/div[1]/div/form/div/div[1]/div[2]/div/div[1]/div[4]/div[1]/span[1]/label')
    seoul_check.click()   # 언론사 서울 지정
    time.sleep(3)
    period = wd.find_element(By.XPATH, '/html/body/div[1]/header/div[1]/div/form/div/div[1]/div[2]/div/div[1]/div[1]/a')
    period.click()   # 기간 선택
    period_start = wd.find_element(By.XPATH, '/html/body/div[1]/header/div[1]/div/form/div/div[1]/div[2]/div/div[1]/div[2]/div/div[2]/div/div[1]/input')
    for _ in range(10):
        period_start.send_keys(Keys.BACK_SPACE)  # 기존 입력값 삭제
    time.sleep(3)
    period_start.send_keys(f'{yesterday}')   # 하루전 날짜 입력
    time.sleep(3)
    apply_option = wd.find_element(By.XPATH, '/html/body/div[1]/header/div[1]/div/form/div/div[1]/div[2]/div/div[4]/div[2]/button[2]')
    apply_option.click()  # 기간, 언론사 세부검색 적용
    time.sleep(3)

    # 1페이지
    for i in range(1,11):
        titles.append(wd.find_elements(By.XPATH, f'/html/body/div[1]/main/div[1]/div[2]/div/div[2]/div[2]/div/div[2]/div[3]/div[5]/div[{i}]/div/div[2]/a/div/strong/span').text)
        urls.append(wd.find_elements(By.XPATH, f'/html/body/div[1]/main/div[1]/div[2]/div/div[2]/div[2]/div/div[2]/div[3]/div[5]/div[{i}]/div/div[2]/div/div/a').text)
    print(titles)
    print(urls)
    # articles = wd.find_elements(By.CLASS_NAME, 'news-item')  # 리스트 형태로 news-item이란 클래스명을 태그를 가져옴
    # for i in articles:
    #     upload_t = i.get_attribute('data-id')  # 가져온 tag내에서 data-id라는 변수의 값을 가져옴
    #     print(type(upload_t))
    #     if int(upload_t[9:]) >= int(yesterday.strftime("%Y%m%d"))*1000000000+153000000:  # 전일 장마감 이후부터


# 장마감 이후(18:00) ~ 장 시작 전(08:30)
#/html/body/div[1]/main/div[1]/div[2]/div/div[2]/div[2]/div/div[2]/div[3]/div[5]/div[5]
# beautifulsoup 이용하여 div.news-item.string? 이 00000000(8글자).20221123120012345(날짜+시간)범위 내에 있는 걸로


''' 기본값이 현재시각이라서 굳이 안바꿔도됨
    period_end = wd.find_element(By.XPATH,'/html/body/div[1]/header/div[1]/div/form/div/div[1]/div[2]/div/div[1]/div[2]/div/div[2]/div/div[3]/input')
    for _ in range(10):
        period_end.send_keys(Keys.BACK_SPACE)  # 기존 입력값 삭제
    time.sleep(3)
    period_end.send_keys(f'{now}')  # 하루전 날짜 입력
    
    마지막 검색버튼 클릭, 상세검색 적용으로 불필요
    time.sleep(3)
    search_button = wd.find_element(By.XPATH, '//*[@id="news-search-form"]/div/div[1]/div[1]/button')
    search_button.click() # 검색버튼 클릭
    time.sleep(3)
    
    
'''
# 스크랩하고 뒤로가기 다시 검색 for문이 끝날때 까지  엑셀파일에 스크랩한 링크들을 추가를 한다 리스트형태로

# 기사 스크랩 방법
# 1. 기사 url 추출
# 2. 기사 스크린 캡쳐
# 3. 기사 내용 복사하여 추출
'''
html = wd.page_source #문제4) 괄호를 채우세요! 실행시 괄호 삭제
soup = BeautifulSoup(html, 'html.parser')
print(soup.prettify())
'''