"""
Отсортировать полезности из логов, ненужное удалить
"""
import os
from service_lib.init_service import init_service, close_log
from service_lib.relog import relog
from service_lib.alerts import send_msg


config_seed = os.path.dirname(os.path.abspath(__file__))
config, nohup_logger, nohup_file = init_service(config_seed, True)

relog(True, config, nohup_logger)
send_msg(config['alerts']['machine_name'] + ': did relog procedure', config=config)

close_log(nohup_file)
