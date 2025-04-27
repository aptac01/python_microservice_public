"""
Этот файл будет выполняться master-процессом uwsgi каждую минуту.
Практической ценности не имеет, нужно исключительно для тестов и отладки.
"""
from service_lib.periodic_tasks import test_test


test_test()
