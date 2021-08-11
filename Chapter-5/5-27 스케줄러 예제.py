from apscheduler.schedulers.background import BackgroundScheduler

schedule = BackgroundScheduler()

def scheduleTest():
    print(1)

schedule.add_job(scheduleTest, 'cron', second="*/2", id="job")

print("스케줄러 시작")
schedule.start()
print("스케줄러 종료?!")