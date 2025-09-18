import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import traceback

class SheetSaver:
    def __init__(self, config):
        self.config = config
        self._setup_sheets()

    def _setup_sheets(self):
        # sheets_config = self.config.get('google_sheets', {})
        creds_file     = self.config.get('GOOGLE_SHEETS_CREDENTIALS', '')
        sheet_name     = self.config.get('GOOGLE_SHEETS_NAME', '크롤링 결과 테스트')
        spreadsheet_id = self.config.get('spreadsheet_id', None)
        
        if not creds_file:
            self.client = None
            return
        
        try:
            # 1) 인증
            scopes = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]
            creds  = Credentials.from_service_account_file(creds_file, scopes=scopes)
            client = gspread.authorize(creds)
            
            # 2) 시트 열기 or 생성
            if spreadsheet_id:
                try:
                    sheet = client.open_by_key(spreadsheet_id)
                except gspread.SpreadsheetNotFound:
                    sheet = client.create(sheet_name)
            else:
                try:
                    sheet = client.open(sheet_name)
                except gspread.SpreadsheetNotFound:
                    sheet = client.create(sheet_name)
            
            sheet.share(
                creds.service_account_email,
                perm_type='user',
                role='writer'
            )
            print("연결된 시트 URL:", sheet.url)
            print("시트 ID:", sheet.id)
            
            # 4) 워크시트 가져오기 및 헤더 세팅
            worksheet = sheet.get_worksheet(0)
            if not worksheet:
                worksheet = sheet.add_worksheet(title="결과", rows=1000, cols=20)
            
            if not worksheet.row_values(1):
                worksheet.append_row(["타임스탬프", "URL", "제목", "성공 여부", "오류"])
            
            # 5) 인스턴스 변수에 저장
            self.creds     = creds
            self.client    = client
            self.sheet     = sheet
            self.worksheet = worksheet

        except Exception as e:
            print(f"Google Sheets 설정 실패: {e}")
            traceback.print_exc()
            self.client = None    
    
    def save_result(self, results):
        if not self.client:
            return False
        
        try:
            for result in results:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                url = result.get('url', '')
                title = result.get('title', '')
                success = "성공" if result.get('success', False) else "실패"
                error = result.get('error', '')
                
                self.worksheet.append_row([timestamp, url, title, success, error])
            return True
        except Exception as e:
            print(f"Google Sheets 저장 실패: {str(e)}")
            return False
