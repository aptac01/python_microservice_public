"""
Тестовый таск для показа работы с остановкой worker'ов uwsgi
"""
import os
from service_lib.init_service import init_service, close_log
from service_lib.periodic_tasks import on_pause, action_on_pause


config_seed = os.path.dirname(os.path.abspath(__file__))
other_config, nohup_logger, nohup_file = init_service(config_seed, True)

action_on_pause(other_config, nohup_logger, on_pause)

close_log(nohup_file)
