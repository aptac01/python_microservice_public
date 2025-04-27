"""
Методы сервиса, относящиеся к бизнес-логике
"""
from .client_errors import generic_service_error


def ping_pong(request_id, args):
    """
    Выдать тестовые данные
    """

    result = {}

    # Представим, что это - сложная бизнес логика
    if args.get('marco', None) is not None \
            and args.get('marco', None) == 'polo':
        result = {'polo': 'marco'}

    if args.get('ping', None) is not None \
            and args.get('ping', None) == 'pong':
        result = {'pong': 'ping'}

    if args.get('get_error', None) is not None:
        result = generic_service_error(request_id, 'Ошибка сгенерирована по запросу', args)

    result_dict = {
        'jsonrpc': '2.0',
        'result': result,
        'id': request_id
    }

    return result_dict
