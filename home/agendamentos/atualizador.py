from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from home.agendamentos.agendador import teste, gera_escala_zerada

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(teste, 'interval', hours=5)
    scheduler.add_job(gera_escala_zerada, 'interval', hours=5)
    scheduler.start()
    