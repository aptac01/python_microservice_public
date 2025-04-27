#!env/bin/python
# coding: utf-8

"""
Скрипт для удобного управления сервисом
"""

import os
from service_lib.init_service import init_service, show_info, close_log
from service_lib.argument_parser import parse_arguments
from service_lib.service_stuff import check_status, generate_ruffles, start_service, stop_service, restart_service
from service_lib.testing import integration_tests, unit_tests
from service_lib.relog import relog

config, nohup_logger, nohup_file = init_service(__file__)
args = parse_arguments(config, actions=[
        'start',
        'stop',
        'restart',
        'hot_restart',
        'status',
        'tests',
        'ruffles',
        'relog',
    ])

nohup_logger.log('----------------- Service managing operation start -----------------')

# запоминаем текущий каталог, позже в него вернёмся
current_working_directory = os.getcwd()
os.chdir(config['api_directory'])

show_info(nohup_logger)

if args.action == 'start':
    start_service(args.consul, config, nohup_logger, nohup_file)

elif args.action == 'stop':
    stop_service(args.consul, config, nohup_logger, nohup_file)

elif args.action == 'restart':
    stop_service(args.consul, config, nohup_logger, nohup_file)
    start_service(args.consul, config, nohup_logger, nohup_file)

elif args.action == 'hot_restart':
    restart_service(config, nohup_logger, nohup_file)

elif args.action == 'status':
    check_status(config, nohup_logger)

elif args.action == 'tests':
    integration_tests(config, nohup_logger)
    unit_tests(config, nohup_logger)

elif args.action == 'ruffles':
    generate_ruffles(config, nohup_logger)

elif args.action == 'relog':
    relog(args.relog, config, nohup_logger)

# меняем каталог обратно как было
os.chdir(current_working_directory)

nohup_logger.log('================= Service managing operation finish ================')

close_log(nohup_file)
