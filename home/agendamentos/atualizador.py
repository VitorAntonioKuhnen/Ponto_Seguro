from apscheduler.schedulers.background import BackgroundScheduler
from home.agendamentos.agendador import gera_escala_zerada, get_api_feriados, confereRegistros, remov_Process_started
from datetime import datetime as hora, timedelta

def start():
    
    scheduler = BackgroundScheduler()
    
    scheduler.add_job(get_api_feriados, 'cron', month='1', day='1', hour='0', minute='0')
    scheduler.add_job(gera_escala_zerada, 'cron', hour=0)
    scheduler.add_job(confereRegistros, 'cron', hour=0, minute=30)
    # scheduler.add_job(gera_escala_zerada, 'interval', seconds= 10)
    # scheduler.add_job(confereRegistros, 'interval', seconds= 30)
    scheduler.add_job(remov_Process_started, 'date', run_date=hora.now() + timedelta(seconds=5))
    scheduler.start()
    