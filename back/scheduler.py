import schedule
import time
import threading

class Scheduler:
    def __init__(self, config, crawler):
        self.config = config
        self.crawler = crawler
        self.schedule_thread = None
        self.running = False
    

    def _run_job(self):
      results = [
          {"url": "https://example.com/a", "title": "임시 A", "success": True},
          {"url": "https://example.com/b", "title": "임시 B", "success": False, "error": "테스트 오류"},
      ]
      print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 세이버 배치 실행")
      ok = self.crawler.save_result(results)
      print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 저장 {'성공' if ok else '실패'}")

    def _run_scheduler(self):
        while self.running:
            schedule.run_pending()
            time.sleep(1)
    
    def set_schedule(self, times):
        schedule.clear()
        
        for time_str in times:
            schedule.every().day.at(time_str).do(self._run_job)
        
        self.config.update({'schedule_times': times})
        
        if not self.running:
            self.start()
    
    def get_schedule(self):
        return self.config.get('schedule_times', [])
    
    def start(self):
        if not self.running:
            self.running = True
            self.schedule_thread = threading.Thread(target=self._run_scheduler)
            self.schedule_thread.daemon = True
            self.schedule_thread.start()
    
    def stop(self):
        self.running = False
        if self.schedule_thread:
            self.schedule_thread.join(timeout=1)
