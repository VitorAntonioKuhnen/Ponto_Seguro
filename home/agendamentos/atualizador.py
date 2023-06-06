from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from home.agendamentos.agendador import teste

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(teste, 'interval', minutes=1)
    scheduler.start()
    