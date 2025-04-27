"""
Немного методов, нужных для работы, но не нужных клиентам
"""
from flask import current_app as app
from service_lib.jsonrpc_stuff import send_request
from service_lib.various_stuff import deep_get


def access_authenticate(request_id, args):
    """
    Проксирует запрос к сервису авторизации
    """

    args_to_send = {
        **args,
        **{'app': app.config['SERVICE_NAME']}
    }

    res = send_request('access.authenticate', args_to_send, app.config['AUTH_URI'], None, request_id)
    return res


def check_token(request_id, token, get_user_info=False):
    """
    Проверка токена на валидность.
    Опционально - с получением инфы о пользователе(права, группа и т.д.)
    """

    uri = app.config['AUTH_URI']

    res1 = send_request('access.checkToken', {
        'accessToken': token
    }, uri, None, request_id)
    valid = deep_get(res1, 'result.valid', False)

    if valid and get_user_info:
        res2 = send_request('access.getUserInfo', {
            'accessToken': token
        }, uri, None, request_id)
        user = res2.get('result')
    else:
        user = None

    return {
        'valid': valid,
        'userInfo': user,
    }


def get_uwsgi_workers(request_id):
    """
    Статистика по текущим worker'ам от uWSGI
    """
    # при запуске uwsgi создает/добавляет "виртуальный" пакет,
    # для управления процессом и доступом ко всяким плюшкам
    # noinspection PyUnresolvedReferences
    import uwsgi

    res = []
    uwsgi_workers = uwsgi.workers()
    for each in uwsgi_workers:
        res.append(each['pid'])

    res.append(uwsgi.masterpid())

    result_dict = {
        'jsonrpc': '2.0',
        'result': res,
        'id': request_id
    }

    return result_dict
