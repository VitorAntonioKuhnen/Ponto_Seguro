from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from home.agendamentos.agendador import gera_escala_zerada, get_api_feriados, confereRegistros

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(get_api_feriados, 'cron', month='1', day='1', hour='0', minute='0')
    scheduler.add_job(gera_escala_zerada, 'cron', hour=0)
    # scheduler.add_job(gera_escala_zerada, 'interval', seconds= 5)
    scheduler.start()
    