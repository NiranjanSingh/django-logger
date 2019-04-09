"""
This module is largely inspired by django-rest-framework settings.

Settings for the django logging are all namespaced in the DJANGO_LOGGER setting.
For example your project's `settings.py` file might look like this:

DJANGO_LOGGER = {
    "IGNORE_PARAMS":
        ['password','username',],
    "APP":
        "APP_NAME",
}

This module provides the `DjangoLoggerSettings` object, that is used to access
Django Logger settings, checking for user settings first, then falling
back to the defaults.
"""
from __future__ import unicode_literals

import copy
import json
import logging

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from .logformat import BASE_LOGGING_FORMAT

USER_SETTINGS = getattr(settings, "DJANGO_LOGGER", None)

# List of settings that cannot be empty
MANDATORY = (
    "APP_NAME",  # application name
    "LOGGER_NAME",  # logger name
    "MAIL_LOGGER_NAME",  # mail logger name
)

DEFAULTS = {
    "SECURE_PARAMS": (),
}


class DjangoLoggerSettings(object):
    """
    A settings object, that allows Django Logger settings to be accessed as properties.

    """

    def __init__(self, user_settings=None, defaults=None, mandatory=None):

        # Initialises logger properties, as later one's depends on
        # previous one's so don't change the order.

        self.user_settings = user_settings or {}
        self.defaults = defaults or {}
        self.mandatory = mandatory or ()
        self.validate_setting()
        self.user_logger_formatters = {}
        self.HANDLER = self.get_handler()
        self.LOGGING_FORMAT = self.get_logger_format(BASE_LOGGING_FORMAT)
        self.GLOBAL = {}

    def __getattr__(self, attr):

        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults

            if attr not in self.defaults.keys():
                raise ImproperlyConfigured("Invalid DjangoLogger setting: %r." % (attr))

            val = self.defaults[attr]

        # Cache the result
        setattr(self, attr, val)

        return val

    def _construct_logger_format(self, format):

        for key, val in format.items():

            if val == {}:
                format[key] = '%(' + key + ')s'
                self.user_logger_formatters[key] = dict

            elif not val:
                format[key] = '%(' + key + ')s'
                self.user_logger_formatters[key] = str

            elif isinstance(val, dict):
                format[key] = self._construct_logger_format(val)

            elif val in (int,):
                format[key] = '%(' + key + ')d'
                self.user_logger_formatters[key] = int

            elif val in (str, dict):
                format[key] = '%(' + key + ')s'
                self.user_logger_formatters[key] = str

            elif val in (float,):
                format[key] = '%(' + key + ').2f'
                self.user_logger_formatters[key] = float

        return format

    def get_logger_format(self, base_format):

        APP_NAME = self.user_settings.get('APP_NAME')
        DATA_KEY = self.user_settings.get('NAMESPACE_KEY', APP_NAME.upper() + "_DATA")

        logging_format = json.dumps(copy.deepcopy(base_format))

        # replace path names as per settings
        logging_format = logging_format \
            .replace('$PATH_APP_NAME', APP_NAME) \
            .replace('$PATH_LOGGER_NAME', self.user_settings.get('LOGGER_NAME')) \
            .replace('$PATH_MAIL_LOGGER_NAME', self.user_settings.get('MAIL_LOGGER_NAME'))

        logging_format = json.loads(logging_format)

        if self.user_settings.get('FILENAME'):
            logging_format['handlers']['console']['filename'] = self.user_settings.get('FILENAME')
            logging_format['handlers']['console']['mode'] = self.user_settings.get('FILEMODE', "w")

        _user_format = copy.deepcopy(self.user_settings.get('LOGGING_FORMAT', {}))
        user_format = {}

        if not _user_format:
            user_format[DATA_KEY] = {"MESSAGE": dict}

        elif "MESSAGE" not in _user_format:
            _user_format.update({"MESSAGE": dict})
            user_format[DATA_KEY] = copy.deepcopy(_user_format)

        else:
            user_format[DATA_KEY] = _user_format

        user_format = self._construct_logger_format(user_format)

        _detailed_log_format = logging_format['formatters']['detailed_log_track']['format']
        _json_detailed_log_format = json.loads(_detailed_log_format)

        _json_detailed_log_format.update(user_format)

        # replace capital or small `message` formatters with correct one
        _detailed_log_format = json.dumps(_json_detailed_log_format) \
            .replace('\n', '').replace(' ', '') \
            .replace('\"%(MESSAGE)s\"', "%(message)s") \
            .replace('\"%(message)s\"', "%(message)s") \
            .replace('\"%(trace)s\"', "%(trace)s")

        # Formatting by finding regex and replacing
        import re
        _detailed_log_format = re.sub('\"%\((?P<name>[a-zA-Z]*)\)(?P<formatter>[d]|.2f)\"',
                                      '%(\g<name>)\g<formatter>',
                                      _detailed_log_format)

        logging_format['formatters']['detailed_log_track']['format'] = _detailed_log_format

        return logging_format

    def get_handler(self):
        # Sets handler for log format if filename is given
        # in configuration FileHandler will be used else
        # StreamHandler

        if self.user_settings.get('FILENAME'):
            return logging.FileHandler
        else:
            return logging.StreamHandler

    def validate_setting(self):

        # validate mandatory settings
        for attr in self.mandatory:
            if not attr in self.user_settings or not self.user_settings.get(attr):
                raise ImproperlyConfigured("DjangoLogger setting: %r is mandatory" % attr)
            # ImproperlyConfigured

        # validate logger format
        if not isinstance(self.user_settings.get('LOGGING_FORMAT', {}), dict):
            raise ImproperlyConfigured("DjangoLogger settings LOGGING_FORMAT must be a %r" % type({}))


logger_settings = DjangoLoggerSettings(USER_SETTINGS, DEFAULTS, MANDATORY)
