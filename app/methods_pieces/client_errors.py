"""
Ошибки, возвращаемые клиентам
"""

import json
from flask import current_app as app


def returned_error(request_id, error_code, message, data=None, args=None):
    """
    Общая ошибка, для однообразности
    """
    error_text = {
        'jsonrpc': '2.0',
        'error': {
            'code': error_code,
            'message': message,
            'data': data,
            'args': args
        },
        'id': request_id
    }

    app.logger.error(json.dumps(error_text, ensure_ascii=False))
    return error_text


def parse_error(request_id, data=None):
    """
    Ошибка с кодом -32700,
    возникает когда во входном json ошибка
    """
    e_code = -32700
    e_msg = 'Parse error'
    return returned_error(request_id, e_code, e_msg, data)


def invalid_request_error(request_id, data=None):
    """
    Ошибка с кодом -32600,
    возникает когда входной json не соответствует спецификации jsonrpc 2.0
    """
    e_code = -32600
    e_msg = 'Invalid request error. Request is not up to spec with jsonrpc 2.0'
    return returned_error(request_id, e_code, e_msg, data)


def method_not_found_error(request_id, data=None):
    """
    Ошибка с кодом -32601,
    возникает когда обозначенный в запросе метод не найден
    """
    e_code = -32601
    e_msg = 'Method not found. The method does not exist or not available.'
    return returned_error(request_id, e_code, e_msg, data)


def invalid_params_error(request_id, data=None):
    """
    Ошибка с кодом -32602,
    возникает когда переданы неверные параметры
    """
    e_code = -32602
    e_msg = 'Invalid method parameter(s).'
    return returned_error(request_id, e_code, e_msg, data)


def generic_service_error(request_id, data=None, args=None):
    """
    Пример просто ошибки, не из спеков jsonrpc 2.0
    """
    e_code = 69000
    e_msg = 'Какая-то ошибка'
    return returned_error(request_id, e_code, e_msg, data, args)


def token_error(request_id, data=None, args=None):
    """
    Ошибка при валидации токена
    """
    e_code = 2
    e_msg = 'Invalid token'
    return returned_error(request_id, e_code, e_msg, data, args)
