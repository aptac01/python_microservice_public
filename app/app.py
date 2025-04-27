#!env/bin/python
# coding: utf-8

"""
Модуль основного приложения, который паралелится через uwsgi
Теоретически, можно запустить его напрямую (в dev-окружении), но иногда это неэффективно,
или (как в случае с экспортом метрик в prometheus) работает некорректно (смотри отличия
prometheus_flask_exporter.multiprocess от prometheus_flask_exporter)
"""

import os
import datetime
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, jsonify, request
from prometheus_flask_exporter.multiprocess import UWsgiPrometheusMetrics

from service_lib.prometheus_stuff import method_to_group_by_fe021e44
from service_lib.service_stuff import parse_config
from service_lib.various_stuff import is_iterable, get_module_local_functions

from app_pieces import *
from methods import parse_error, invalid_request_error
from methods import method_not_found_error, token_error, check_token

from methods_pieces import method_calls

# --------------- flask      ---------------
app = Flask(__name__)

# --------------- app config ---------------
config = parse_config(f'{os.getcwd()}/config.yaml')
app.config.update(config)

# --------------- prometheus ---------------
metrics = UWsgiPrometheusMetrics(app,
                                 group_by=method_to_group_by_fe021e44,
                                 defaults_prefix='python_rest',
                                 static_labels={'service': app.config['SERVICE_NAME'],
                                                'subsystem': app.config['SERVICE_NAME']}
                                 )

# --------------- logs       ---------------
LOG_PATH = os.getcwd() + '/log/'
LOG_FILENAME = f'{LOG_PATH}example.log'
handler = RotatingFileHandler(LOG_FILENAME, backupCount=1, maxBytes=500000)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)
# --------------- app        ---------------

# пути определенные в отдельных файлах
app.register_blueprint(app_pieces)


@app.route('/', methods=['POST'])
def another_handler():
    """
    Вызвать main_packet_handler без параметра
    """
    return main_packet_handler(None)


@app.route('/<var_route>', methods=['POST'])
def main_packet_handler(var_route):
    """
    Обработать запрос(ы) к сервису.
    """
    if app.config.get('ALLOW_BATCHES', False):
        return jsonify(handle_batch(request.json, var_route))
    else:
        return jsonify(handle_single_obj(request.json, var_route))


def handle_batch(request_json, var_route):
    """
    Обработает как единственный запрос ({....data...}),
    так и batch запрос ([{}, {}, {}])
    """

    result_batch = []
    unbatch_needed = False

    # оборачиваем одиночный запрос в []
    if (not isinstance(request_json, list)) \
            and isinstance(request_json, dict):
        unbatch_needed = True
        request_json = [request_json]

    # отвечаем пустым ответом на пустые запросы (например, ping)
    if not is_iterable(request_json):
        return result_batch

    for batch_elem in request_json:

        result_batch.append(handle_one_obj(batch_elem, var_route))

    if unbatch_needed:
        result_batch = result_batch[0]
    return result_batch


def handle_single_obj(request_json, var_route):
    """
    Обработает единственный запрос ({....data...}), никаких batch'ей.
    Если будет batch - выдаст текстовую ошибку
    """

    # отвечаем пустым ответом на пустые запросы (например, ping)
    if not is_iterable(request_json):
        return {}

    if isinstance(request_json, list):
        return 'Этот сервис не работает с batch-запросами.'

    return handle_one_obj(request_json, var_route)


def handle_one_obj(request_json, var_route):
    """
    Обработка одного пакета
    """

    if not is_iterable(request_json):
        return invalid_request_error('got no id!', 'Request object is not even iterable! ')

    # если при парсинге json из запроса произошла ошибка - пытаемся помочь пользователю понять где она
    if 'e' in request_json \
            and 'on_json_loading_failed' in request_json:
        return parse_error(None, str(request_json['e']))

    # ошибка при несоблюдении jsonrpc2
    if ('jsonrpc' not in request_json
            or request_json['jsonrpc'] != '2.0'
            or 'id' not in request_json
            or 'method' not in request_json):
        return invalid_request_error(
            request_json.get('id', 'got no id!')
        )

    request_id = request_json['id']
    method_from_client = request_json['method']
    params = request_json.get('params', {})

    # проверка токена
    if app.config.get('USING_AUTH', True) \
            and method_from_client != 'access.authenticate':
        token = params.get('token', None)
        if token is None:
            return token_error(request_id)
        token_result = check_token(request_id, token)
        if not token_result['valid']:
            return token_error(request_id)
    else:
        token_result = {}

    datetime_now = datetime.datetime.now()
    # адрес приложения
    ip0 = request.remote_addr
    # адрес пользователя
    ip1 = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

    app.logger.info(f'{datetime_now.strftime("%Y-%m-%dT%H:%M:%S")}: remote address: {ip0} real IP: {ip1} '
                    + f'method: {method_from_client}')

    method_name_escaped = method_from_client.replace('.', '_dot_')

    if method_name_escaped in get_module_local_functions(method_calls):

        # вызов функции соответствующей методу из модуля method_calls
        result = getattr(method_calls, method_name_escaped)(
            request_id=request_id,
            params=params,
            var_route=var_route,
            token_result=token_result,
        )
        return result

    else:
        return method_not_found_error(request_id)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=config['local_port'],
        debug=False
    )
