import django_logger
from django.http.response import HttpResponse
import logging

try:
    from django.views import View
except ImportError:
    # for django >= 1.8
    from django.views.generic import View

logger = logging.getLogger('test')


class Testview(View):

    def get(self, request, **kwargs):
        django_logger.clear_global_log()

        django_logger.set_global_logs(
            {'c': {'x': object}, 'C': "something else", 'INT': 10, 'FLOAT': 9.32, 'a': "some text"})

        logger.info("Just to test global logs.")

        django_logger.clear_global_log()

        return HttpResponse()
