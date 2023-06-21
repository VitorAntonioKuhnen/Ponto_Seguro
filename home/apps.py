from django.apps import AppConfig
import os

class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'

    # def ready(self):
    #     from home.agendamentos.atualizador import  start
    #     start()
    
    def ready(self):
        if not os.path.isfile('process_started.txt'):
            self.start_process()
            self.create_state_file()

    def start_process(self):
        from home.agendamentos.atualizador import start
        start()

    def create_state_file(self):
        with open('process_started.txt', 'w') as file:
            file.write('Process started')