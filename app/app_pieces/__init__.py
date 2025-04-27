"""
Здесь нужно импортировать все файлы из этой папки
"""
from flask import Blueprint

app_pieces = Blueprint('app_pieces', __name__)

from . import swagger
from . import error_handlers
from . import metrics
