"""
Обернутые вызовы методов. Одна функция - один вызов.

Здесь должна быть проверка прав юзеров, предварительная валидация и прочее,
что не нужно в реализации основной части метода.

Названия функций составляются из названия метода для клиентов
заменой символа точки на _dot_ ("." => "_dot_").
"""
from .main_methods import ping_pong
from .system_methods import access_authenticate, get_uwsgi_workers
from .client_errors import invalid_params_error


def pingpong(**kwargs):
    request_id = kwargs['request_id']
    params     = kwargs['params']
    return ping_pong(request_id, params)


def access_dot_authenticate(**kwargs):   # noqa

    request_id = kwargs['request_id']
    params = kwargs['params']
    var_route = kwargs['var_route']

    if ('login' in params or 'userId' in params) \
            and 'password' in params \
            and var_route == 'login':
        return access_authenticate(request_id, params)
    else:
        return invalid_params_error(request_id)


def service_dot_uwsgi_stats(**kwargs):

    request_id = kwargs['request_id']

    return get_uwsgi_workers(request_id)
