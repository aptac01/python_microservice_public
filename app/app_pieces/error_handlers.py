"""
Обработчики ошибок на запросы
"""
from . import app_pieces
from flask import jsonify, Request, make_response


# noinspection PyUnusedLocal
@app_pieces.app_errorhandler(404)
def not_found(error):
    """
    Обработать ошибку с кодом 404
    """
    return make_response(jsonify({'error': 'Not found'}), 404)


# noinspection PyUnusedLocal
def on_json_loading_failed(self, e):
    """
    Вернуть специальную метку и описание возникшей ошибки в объекте запроса
    в случае, если не удалось спарсить json из запроса клиента
    """
    if e is not None:
        return {
            'e': e,
            'on_json_loading_failed': 1
        }


Request.on_json_loading_failed = on_json_loading_failed
