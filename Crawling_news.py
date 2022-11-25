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

# 시간 변수 선언
now = dt.datetime.now().date()  # 오늘
yesterday = now - dt.timedelta(1)  # 전날

# Current_own.py에서 저장한 user_infos.xlsx에서 종목명만 불러와 리스트에 저장
stock_df = list(pd.read_excel('user_infos.xlsx', engine='openpyxl', header=0, index_col=0)['종목명'][:])



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
    time.sleep(1)
    period_start.send_keys(f'{yesterday}')   # 하루전 날짜 입력
    time.sleep(1)
    apply_option = wd.find_element(By.XPATH, '/html/body/div[1]/header/div[1]/div/form/div/div[1]/div[2]/div/div[4]/div[2]/button[2]')
    apply_option.click()  # 기간, 언론사 세부검색 적용
    time.sleep(3)

    # 총 기사 개수를 파악 후 페이지를 넘기며 해당 페이지의 기사제목과 링크를 가져와 각 리스트에 저장
    n = int(wd.find_element(By.XPATH,'/html/body/div[1]/main/div[1]/div[2]/div/div[2]/div[2]/div/div[2]/div[3]/div[3]/h3/span[6]').text) // 10 + 1  # 페이지 수
    m = int(wd.find_element(By.XPATH,'/html/body/div[1]/main/div[1]/div[2]/div/div[2]/div[2]/div/div[2]/div[3]/div[3]/h3/span[6]').text) % 10  # 마지막 페이지 기사 개수
    for pg in range(1, n+1):  # 전체 페이지 수 만큼 반복
        if n == 1 and m == 0:  # 기사가 0개
            break
        if (n == 1 or pg == n) and m != 0:  # 기사 10개 미만이거나 마지막 페이지 일 때
            articles = wd.find_elements(By.CLASS_NAME, 'news-item')  # 리스트 형태로 news-item이란 클래스명을 태그를 가져옴
            time.sleep(1)
            for j in range(1, m+1):
                upload_t = int(articles[j - 1].get_attribute('data-id')[9:])  # 가져온 tag내에서 data-id라는 변수의 값을 가져옴
                d_limit = int(yesterday.strftime("%Y%m%d")) * 1000000000 + 153000000  # 시간 제한
                #print(d_limit)
                #print(upload_t)
                if upload_t >= d_limit:  # 전일 장마감 이후 작성된 기사부터 추출
                    titles.append(wd.find_element(By.XPATH, f'/html/body/div[1]/main/div[1]/div[2]/div/div[2]/div[2]/div/div[2]/div[3]/div[5]/div[{j}]/div/div[2]/a/div/strong/span').text)  # 기사 제목 추출
                    time.sleep(1)
                    try:
                        url.append(wd.find_element(By.XPATH, f'/html/body/div[1]/main/div[1]/div[2]/div/div[2]/div[2]/div/div[2]/div[3]/div[5]/div[{j}]/div/div[2]/div/div/a').get_attribute('href'))  # 기사 링크 추출
                        time.sleep(1)
                    except:
                        urls.append('원본 link 확인 불가')
        else:   # 기사 개수가 10의 배수이거나 마지막 페이지가 아닐 때
            articles = wd.find_elements(By.CLASS_NAME, 'news-item')  # 리스트 형태로 news-item이란 클래스명을 태그를 가져옴
            time.sleep(1)
            for k in range(1, 11):  # 페이지 당 최대 표시 기사 갯수 10개
                upload_t = int(articles[k-1].get_attribute('data-id')[9:])  # 가져온 tag내에서 data-id라는 변수의 값을 가져옴
                d_limit = int(yesterday.strftime("%Y%m%d")) * 1000000000 + 153000000  # 시간 제한
                # print(d_limit)
                # print(upload_t)
                if upload_t >= d_limit:  # 전일 장마감 이후 작성된 기사부터 추출
                    titles.append(wd.find_element(By.XPATH, f'/html/body/div[1]/main/div[1]/div[2]/div/div[2]/div[2]/div/div[2]/div[3]/div[5]/div[{k}]/div/div[2]/a/div/strong/span').text)  # 기사 제목 추출
                    time.sleep(1)
                    try:
                        urls.append(wd.find_element(By.XPATH, f'/html/body/div[1]/main/div[1]/div[2]/div/div[2]/div[2]/div/div[2]/div[3]/div[5]/div[{k}]/div/div[2]/div/div/a').get_attribute('href'))  # 기사 링크 추출
                        time.sleep(1)
                    except:
                        urls.append('원본 link 확인 불가')
            wd.find_element(By.XPATH,'/html/body/div[1]/main/div[1]/div[2]/div/div[2]/div[2]/div/div[2]/div[3]/div[7]/div[1]/div/div/div/div[4]/a').click()  # 다음페이지로 이동
            time.sleep(3)  # 페이지가 로드 되기 전 클릭하는걸 막아주는 역할
    print(titles)
    print(urls)
    # url과 title을 csv파일 형태로 저장
    if len(titles) != 0:
        df = pd.DataFrame(titles, columns=['기사 제목'])
        df['url'] = urls
        df.to_csv("news.csv", index=False)
    else:
        print("검색된 기사가 없습니다.")
    titles, urls = [], []   # 리스트 초기화

    # 빅카인즈 홈페이지로 돌아감
    try:  # 작은 창모드 일때
        wd.find_element(By.XPATH,'/html/body/div[1]/header/div[1]/div/a/button').click()
    except:  # 큰 창모들 일때
        wd.find_element(By.XPATH,'/html/body/div[1]/header/div[1]/div/h1/a/img').click()
# 필요 작업: csv파일로 저장하되 매번 새로운 파일을 만드는게 아니라 dataframe에 이어 붙혀서 인덱스를 검색어로 하는 df를 최종적으로 만든 뒤 파일로 저장하는 작업 필요


# 기본값이 현재시각이라서 굳이 안바꿔도됨
#     period_end = wd.find_element(By.XPATH,'/html/body/div[1]/header/div[1]/div/form/div/div[1]/div[2]/div/div[1]/div[2]/div/div[2]/div/div[3]/input')
#     for _ in range(10):
#         period_end.send_keys(Keys.BACK_SPACE)  # 기존 입력값 삭제
#     time.sleep(3)
#     period_end.send_keys(f'{now}')  # 하루전 날짜 입력
#
#     마지막 검색버튼 클릭, 상세검색 적용으로 불필요
#     time.sleep(3)
#     search_button = wd.find_element(By.XPATH, '//*[@id="news-search-form"]/div/div[1]/div[1]/button')
#     search_button.click() # 검색버튼 클릭
#     time.sleep(3)

# 스크랩하고 뒤로가기 다시 검색 for문이 끝날때 까지  엑셀파일에 스크랩한 링크들을 추가를 한다 리스트형태로

# 기사 스크랩 방법
# 1. 기사 url 추출 (O)
# 2. 기사 스크린 캡쳐 (X)
# 3. 기사 내용 복사하여 추출 (X)
