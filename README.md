# AutoInvest
invest agent

1. Back - flask API server
2. Front - react or index.html
3. DB - google sheet or postgresql
4. batch -> scheduler.py
5. Email Send -> sender.py



### requirements

pip install gspread google-auth pyyaml (google sheet saver temp)
pip install yagmail[all] pyyaml flask (이메일 temp)
pip install python-dotenv (env 관련)
pip install schedule  (batch 관련)


### google requirements

- 앱 비밀번호
  - 2단계 인증 > google 계정 관리 > 보안 > 앱비밀번호 검색 > 앱비밀번호 생성
- 서비스 게정 json 키 생성 : 
  - > Google Cloud : [link](https://console.cloud.google.com/) > 서비스 계정 > 서비스 계정 만들기 
- Google Drive API Enable  : [link](https://console.cloud.google.com/apis/api/drive.googleapis.com/metrics?project=crawlsender&inv=1&invt=AbwSvg)
- Google Sheet API Enable  : [link](https://console.cloud.google.com/marketplace/product/google/sheets.googleapis.com?q=search&referrer=search&inv=1&invt=AbwSvg&project=crawlsender)
- 해당 spreadSheet google 서비스 계정 공유하기

### Google Drive API 한도
Google Drive API는 대부분의 경우 무료로 사용할 수 있습니다.
하지만 사용량 한도를 초과하거나 특정 기능을 사용하면 추가 요금이 부과될 수 있습니다. 

상세 내용:
- 무료 티어: Google Drive API는 기본적으로 무료로 제공됩니다. 
- 할당량: 특정 요청 한도를 넘어서는 경우 추가 비용이 발생할 수 있지만, 일반적으로 추가 비용이 청구되지는 않습니다. 
- 추가 요금: 특정 API 기능이나 Google Cloud Platform의 다른 서비스와 함께 사용할 때 추가 요금이 발생할 수 있습니다. 
- Google Cloud Pricing Calculator: 정확한 가격 책정을 확인하려면 Google Cloud Pricing Calculator를 이용하세요


### Google Sheet 할당량 한도

- Sheets API에는 API 요청에 대해 엄격한 크기 제한이 없지만, Sheets에서 제어할 수 없는 여러 처리 구성요소로 인해 제한이 발생할 수도 있습니다. 요청 속도를 높이려면 최대 페이로드 용량은 2MB로 설정하는 것이 좋습니다.
- Sheets API에는 분당 할당량이 있으며 1분마다 다시 채워집니다. 예를 들어 읽기 요청은 프로젝트별로 분당 300회로 제한됩니다. 앱이 1분에 350개의 요청을 보내면 추가로 50개의 요청이 할당량을 초과하여 429: Too many requests HTTP 상태 코드 응답입니다. 

할당량
- 읽기 요청	
  - 프로젝트별 분당 할당량	300
  - 프로젝트별 사용자당 분당 할당량	60
- 쓰기 요청	
  - 프로젝트별 분당 할당량	300
  - 프로젝트별 사용자당 분당 할당량	60

### POSTGRESQL 