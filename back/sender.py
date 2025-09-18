import yagmail
from datetime import datetime

class EmailSender:
    def __init__(self, config):
        self.config = config
    
    def send_result(self, results, to=None):
        # email = self.config.get('email', {})
        sender = self.config.get('EMAIL_SENDER', '')
        password = self.config.get('EMAIL_PASSWORD', '')
        recipients = to if to else ''

        if not sender or not password or not recipients:
            return False
        
        try:
            yag = yagmail.SMTP(sender, password)
            subject = f"크롤링 결과 - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            
            html_content = "<h2>크롤링 결과</h2>"
            html_content += "<table border='1' cellpadding='4'><tr><th>URL</th><th>제목</th><th>상태</th></tr>"
            for r in results:
                status = "성공" if r.get('success', False) else f"실패: {r.get('error', '')}"
                html_content += (
                    f"<tr>"
                    f"<td>{r.get('url','-')}</td>"
                    f"<td>{r.get('title','-')}</td>"
                    f"<td>{r.get('age_range', '-')}</td>"
                    f"<td>{r.get('age', '-')}</td>"
                    f"<td>{status}</td>"
                    f"</tr>"
                )
            html_content += "</table>"

            yag.send(to=recipients, subject=subject, contents=html_content)
            return True
        except Exception as e:
            print(f"이메일 전송 실패: {str(e)}")
            return False
