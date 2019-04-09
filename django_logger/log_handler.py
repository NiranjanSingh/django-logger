from __future__ import absolute_import

import threading

from django_logger.settings import logger_settings

"""Data-wrangling for loggers"""
import ast
import json
import logging
import traceback

import arrow
import pytz


def clear_global_log():
    """
    Clears global log, this needs to be called before setting global log
    in order to clear if any previous process would have set any logs.

    """
    logger_settings.GLOBAL = dict()


# Helper function for setting value in global log via crequest in case of django
def set_global_logs(values):
    """
    Sets key, value pair from values dict, in global log

    Parameters
    ----------
    values: <dict>
        Dict containing key:value pair, which needs to be set,
        must be present in DJANGO_LOGGER[`LOGGING_FORMAT`] settings

    Returns
    -------

    Exception: If `key` not present in DJANGO_LOGGER[`LOGGING_FORMAT`] or
               `request` is empty

    True: If successfully sets `val` to `key` in values in global log

    """
    for key in values.keys():
        if key not in logger_settings.user_logger_formatters.keys():
            raise Exception('Key {} not present in config defined {}.'.format(key, logger_settings.user_logger_formatters))

    # setting value in global against current thread
    current_thread = threading.current_thread()
    if not logger_settings.GLOBAL.get(current_thread):
        logger_settings.GLOBAL[current_thread] = {}

    for key,val in values.items():
        logger_settings.GLOBAL[current_thread][key] = val

    return True


class ContextualFilter(logging.Filter):
    """
        Overrides loggging.Filter
        to the logging Context. DOES NOT FILTER ANY LOGS, all logs are passed.
    """

    def filter(self, log_record):
        """Filter messages to be logged.

        Parameters
        ----------
        `log_record` : <logging.LogRecord>
            The log-record to be processed and filtered.

        Returns
        -------
        `True`
            if the `log_record` is to be logged.
        `False`
            if the `log_record` is to be dropped.

        Notes
        -----
        Currently we aren't dropping any logs. This function simply transforms
        the log-record by injecting additional data into it, and prepares keys
        for the log-formatter.
        """

        def _get_key_value(key=None, val_type=None):

            value = None
            current_thread = threading.current_thread()

            if logger_settings.GLOBAL.get(current_thread):
                value = logger_settings.GLOBAL[current_thread].get(key)

            if not value:
                if val_type in (int,):
                    value = 0
                elif val_type in (float,):
                    value = 0.0
                elif val_type in (dict,):
                    value = {}
                else:
                    value = ""

            return value

        def _get_trace():
            trace = ""
            if log_record.levelname in ['ERROR', 'CRITICAL']:
                trace = traceback.format_exc().strip()  # Get the recent stack-trace

            return json.dumps(trace)

        def _get_msg():
            try:
                # `loads` and `dumps` for printing JSON structure in a single line
                json_data = json.loads(log_record.msg)
                msg = json.dumps(json_data)
            except ValueError:
                msg = json.dumps({
                    "TEXT": log_record.msg,
                })
            except TypeError:
                # We tried to `json.loads` something that's not a string
                # Let's print its string-representation
                msg = json.dumps({
                    "OBJ": repr(log_record.msg),
                })
            return msg

        def _get_log_time():
            tz_IST = pytz.timezone(pytz.country_timezones['IN'][0])
            return str(arrow.now(tz=tz_IST).format('YYYY-MM-DDTHH:mm:ss.SSSZZ'))

        log_record.trace = _get_trace()
        log_record.msg = _get_msg()
        log_record.time = _get_log_time()

        # setting values for key log_record
        for key, val_type in logger_settings.user_logger_formatters.items():
            setattr(log_record, key, _get_key_value(key, val_type))

        # Clean message
        try:
            # If case of `exception` level is there we don't want trace print it again
            if log_record.exc_info:
                log_record.exc_info = None  # its checked in python logging (__init__.py) #571 in logging for python 3.5

            log_msg = json.loads(log_record.msg)
            msg = log_msg.get('OBJ', None)
            if msg:
                msg_dict = ast.literal_eval(msg)

                _args = msg_dict.get('ARGS', "")

                if not isinstance(_args, str):
                    _args = repr(_args)

                _kwargs = msg_dict.get('KWARGS', "")
                if not isinstance(_kwargs, str):
                    _kwargs = repr(_kwargs)

                if msg_dict:
                    if 'MESSAGE' in msg_dict:
                        log_record.msg = json.dumps({
                            'TEXT': msg_dict.get('MESSAGE', ''),
                            'ARGS': _args,
                            'KWARGS': _kwargs
                        })
                        log_record.pathname = msg_dict.get('_PATH', log_record.pathname)
                        log_record.funcName = msg_dict.get('_FUNCNAME', log_record.funcName)
                        log_record.lineno = msg_dict.get('_LNO', log_record.lineno)
                    else:
                        log_record.msg = json.dumps({})
        except Exception as e:
            log_record.msg = json.dumps({
                "ERROR": "Exception occurred while parsing `{}`".format(e),
                "MESSAGE": log_record.msg
            })
            pass

        return True  # Don't drop any logs


class ContextHandler(logger_settings.HANDLER):
    """
        Overrides logging.StreamHandler

    """

    def __init__(self, *args, **kwargs):
        logger_settings.HANDLER.__init__(self, *args, **kwargs)
        self.addFilter(ContextualFilter())
