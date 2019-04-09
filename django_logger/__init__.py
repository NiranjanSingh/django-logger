from .log_handler import set_global_logs, clear_global_log
from .settings import logger_settings
from .decorator import FunctionLogger

name = 'django_logger'

LOGGING_FORMAT = logger_settings.LOGGING_FORMAT

__all__ = [LOGGING_FORMAT, FunctionLogger, set_global_logs, clear_global_log]

from setuptools import setup