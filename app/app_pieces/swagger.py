"""
Всё что относится к работе swagger_ui
"""
import os

from . import app_pieces
from flask import send_from_directory, abort
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from prometheus_flask_exporter.multiprocess import UWsgiPrometheusMetrics

from service_lib.service_stuff import parse_config
from service_lib.various_stuff import deep_get

# --------------- config     ---------------
config = parse_config(f'{os.getcwd()}/config.yaml')
sw_enabled = deep_get(config, 'swagger_ui.enabled', None)

# --------------- basic auth ---------------
if sw_enabled:
    auth = HTTPBasicAuth()
    users = {}

    for _sw_user, _sw_passw in deep_get(config, 'swagger_ui.users', {}).items():
        users[_sw_user] = generate_password_hash(_sw_passw)

    @auth.verify_password
    def verify_password(username, password):
        """
        Проверить пароль пользователя.
        """
        if username in users \
                and check_password_hash(users.get(username), password):
            return username

else:
    def dummy_callable(f):
        return f
    auth = type('', (), {})()
    auth.login_required = dummy_callable


@app_pieces.route('/swagger_ui/', methods=['GET'])
@UWsgiPrometheusMetrics.do_not_track()
@auth.login_required
def swagger_ui_slash():
    """
    Показать содержимое docs.yaml в удобном графическом интерфейсе
    """
    if sw_enabled:
        return send_from_directory('../swagger_ui', 'index.html')
    else:
        abort(403)


@app_pieces.route('/swagger_ui/<file>', methods=['GET'])
@UWsgiPrometheusMetrics.do_not_track()
@auth.login_required
def swagger_ui_files(file):
    """
    Скрипты для swaggerUI
    """
    if sw_enabled:
        return send_from_directory('../swagger_ui', file)
    else:
        abort(403)


@app_pieces.route('/docs_scheme', methods=['GET'])
@UWsgiPrometheusMetrics.do_not_track()
@auth.login_required
def swagger_ui_scheme():
    """
    Главная схема для swaggerUI
    """
    if sw_enabled:
        return send_from_directory('../docs', 'docs.yaml')
    else:
        abort(403)


@app_pieces.route('/docs_pieces/<part>', methods=['GET'])
@UWsgiPrometheusMetrics.do_not_track()
@auth.login_required
def swagger_ui_scheme_pieces(part):
    """
    Части схемы для swaggerUI
    """
    if sw_enabled:
        return send_from_directory('../docs/docs_pieces', part)
    else:
        abort(403)
