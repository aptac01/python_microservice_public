from . import app_pieces
from service_lib.prometheus_stuff import get_prometheus_metric_labels
from flask import request


# noinspection PyProtectedMember
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from prometheus_flask_exporter.multiprocess import UWsgiPrometheusMetrics


@app_pieces.route('/ping/')
@UWsgiPrometheusMetrics.do_not_track()
def ping():
    """
    Подтвердить, что сервис "жив", ответить на проверку consul'а
    """
    return 'pong'


@app_pieces.route('/metrics', methods=['GET'])
@UWsgiPrometheusMetrics.do_not_track()
def prometheus_metrics():
    """
    Отдать метрики для prometheus'а
    """

    # noinspection PyProtectedMember
    from prometheus_client import multiprocess, CollectorRegistry

    registry = CollectorRegistry()

    if 'name[]' in request.args:
        registry = registry.restricted_registry(request.args.getlist('name[]'))

    multiprocess.MultiProcessCollector(registry)

    headers = {'Content-Type': CONTENT_TYPE_LATEST}

    metrics_response = generate_latest(registry)
    metrics_response = get_prometheus_metric_labels(metrics_response)

    return metrics_response, 200, headers
