import schedule
from apps.crawling import crawling
import os
import sys

# 경로 추가
sys.path.append(os.path.abspath("../../"))

def run_schedule(s_time = "15:46:00"):
    print("스케쥴링 시작 ")
    schedule.every().day.at(s_time).do(crawling.start_crawling)

    # step4.스캐쥴 시작
    while True:
        schedule.run_pending()