"""
Чистит мусорные файлы, этот скрипт запускается по крону (см. конфиг)
"""
import os
from service_lib.service_stuff import get_date_prefix
from service_lib.init_service import init_service, close_log
from service_lib.relog import delete_logs_and_pfe
from service_lib.alerts import send_msg


config_seed = os.path.dirname(os.path.abspath(__file__))
config, nohup_logger, nohup_file = init_service(config_seed, True)

delete_logs_and_pfe(config)

delete_junk_days = config.get('DELETE_JUNK_CRON_DAYS', 7)
log_str = f'{get_date_prefix(config)}deleted logs and pfe files older than {delete_junk_days} days'
nohup_logger.log(log_str)
send_msg(config['alerts']['machine_name'] + ': ' + log_str, config=config)

close_log(nohup_file)
