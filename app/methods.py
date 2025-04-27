#!env/bin/python
# coding: utf-8

"""
Удобный импорт всех методов из одного модуля.
Здесь нужно подключать все файлы из methods_pieces
"""

from service_lib.various_stuff import get_module_local_functions

from methods_pieces import client_errors
from methods_pieces.client_errors import *   # noqa

from methods_pieces import main_methods
from methods_pieces.main_methods import *    # noqa

from methods_pieces import system_methods
from methods_pieces.system_methods import *  # noqa

__all__ = []
# проксирование всех функций сабмодуля для импорта из корневого модуля
__all__ = __all__ + get_module_local_functions(client_errors)
__all__ = __all__ + get_module_local_functions(main_methods)
__all__ = __all__ + get_module_local_functions(system_methods)
