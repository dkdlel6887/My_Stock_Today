# My_Stock_Today
Free Program. You can check daily price and read reports about stocks you currently own.


### 주요기능
1) 장 시작 전 보유종목들에 관한 기사 link 종합하여 메일로 전파해 줌<br>
   - 기사 검색기간은 전일 장 마감이후 ~ 장 시작 전 30분
   - 기사는 [빅카인즈](https://bigkinds.or.kr)에서 검색하며, selenium 이용
2) Random forest 이용하여 기사의 긍정, 부정적 여부 진단, 비율을 통해 가벼운 예측 진행
3) 로그인하여 보유종목을 입력하고 개인 정보 저장 가능
4) 현재가 및 보유 종목 별 수익률, 손익금 확인 가능

### 사용절차
1) 신규) 회원가입(id, pw, email 기입) + 기능 설명 확인 및 메일 수신 동의<br>
   - 로그인 - 보유종목, 평균매수가, 보유수량 정보 저장 - 관심종목 저장
2) 회원) 로그인 - 보유종목 수정 - 관심종목 수정

### 사용목적
- 자신이 보유 중인 주식 종목들에 대한 기사 종합적으로 확인 가능, 시간 절약

### Structure
1. Common function : 자주 사용하는 기능들 모아 라이브러리화
2. Sign up: 회원가입 절차 구현  ID, pw, email 등의 정보 기입
3. Current own: 현재 보유주식 이름, 평균매수가, 보유수량, 관심종목 정보 기입
4. Sing in: 회원가입한 사용자의 로그인 시스템 구현
5. Crawling news: 사용자가 보유한 주식 관련 기사 검색
6. Stock price: 전일 종가 정보 추출 및 매수가 대비 수익률, 수익금액 계산
7. PN analysis: 검색한 기사의 긍정/부정 정도 판단하여 정보 제공
8. Time check: 메일 or 카카오톡 발송 시간 지정, 추가로 시간관련 작업 수행
9. Send email: 4 ~ 6의 정보 사용자 email로 전송하도록 구현
10. Main: 실제 사용자가 사용할 프로그램 1 ~ 8 기능 종합

- 구현순서: 3 - 5 - 6 - 7 - 8 - 9 - 2 - 4 - 10

### Commit Type
- feat : 새로운 기능 추가, 기존의 기능을 요구 사항에 맞추어 수정<br>
- fix : 기능에 대한 버그 수정<br>
- build : 빌드 관련 수정<br>
- chore : 패키지 매니저 수정, 그 외 기타 수정 ex) .gitignore<br>
- ci : CI 관련 설정 수정<br>
- docs : 문서(주석) 수정<br>
- style : 코드 스타일, 포맷팅에 대한 수정<br>
- refactor : 기능의 변화가 아닌 코드 리팩터링 ex) 변수 이름 변경<br>
- test : 테스트 코드 추가/수정<br>
- release : 버전 릴리즈
