# DON'T CHANGE THE WAY FUNCTION IS BEING CALLED, IF SO THEN DO CHANGE THE TEST CASE DATA AS WELL

import json
import logging

from django.test.client import Client
from django.conf import settings

from django_logger import FunctionLogger
from unittest import TestCase
from test_data import *

LOGGER_CONFIG = settings.DJANGO_LOGGER

logger = logging.getLogger('test')


# Test case: Username, Password both should be secured and printed as `****`
#           as `password` is set in settings and username is mentioned in decorator
@FunctionLogger(secure_args=['username'])
def func_args(username, password):
    return "Username - " + password


# Test case: `username` should be printed in log as given
@FunctionLogger()
def func_kwargs(username, arg1=3):
    return 'username' + str(arg1)


# Test case: Username, Password both should be secured and printed as `****`
#           as `password` is set in settings and username is mentioned in decorator
@FunctionLogger()
def func_blank():
    return "Any Value"


# Test case: To test securing params with different data types
@FunctionLogger(secure_args=['secure_arg'])
def func_secure_args(secure_arg):
    return {'secure_arg': 'something_secured_string_intentionally_keeping_it_big'}


# Test case: Function returns an object
@FunctionLogger()
def func_return_obj():
    return int


def is_dict_verified(first, second):
    try:
        iterator = first.items()
    except AttributeError:
        iterator = first.iteritems()

    for key, value in iterator:

        try:
            if isinstance(value, dict):
                is_verified, error = is_dict_verified(value, second[key])

                if not is_verified:
                    return False, error

            elif value != second[key]:
                return False, (key, value)

        except KeyError:
            return False, (key, value)

    return True, ()


class TestDjangoLogger(TestCase):

    def setUp(self):
        # pass
        # clean example.log if already exists
        try:
            open('example.log', 'w').close()

            # while running another test case have to reset loggers stream to 0
            logger.handlers[0].stream.seek(0)
        except Exception:
            pass

    def check_my_log(self, expected_logs, dynamic_keys=()):
        dynamic_keys += ('PATH', 'LINE', 'TIME', 'LINE',)
        log_file = open('example.log', 'r')  # read binary and check for binary file
        actual_logs = log_file.read().split('\n')  # .lstrip('\x00').split('\n')
        actual_logs.remove('')
        for actual_log, expected_log in zip(actual_logs, expected_logs):

            _json_log = json.loads(actual_log)

            is_verified, error = is_dict_verified(expected_log, _json_log)
            self.assertEqual(is_verified, True, error)

            # check if keys present with some values in it in actual log
            # as they will always change so it can't be tested via predefined test data
            for k in dynamic_keys:
                _error_msg = str(k) + " does not exist in " + repr(_json_log)
                self.assertEqual(k in _json_log.keys(), True, _error_msg)

                _error_msg = str(k) + " does not contain any value in " + repr(_json_log)
                self.assertEqual(len(str(_json_log.get(k))) > 0, True, _error_msg)

        log_file.close()

    def test_func_blank(self):
        func_blank()
        self.check_my_log(FUNC_BLANK_LOG)

    def test_func_args(self):
        func_args('test_username', 'test_password')
        self.check_my_log(FUNC_ARGS_LOG)

    def test_func_kwargs_with_values(self):
        func_kwargs('test_username', arg1=10)
        self.check_my_log(FUNC_KWARGS_LOG_WITH_VALUES)

    def test_func_kwargs_with_defaults(self):
        func_kwargs('test_username')
        self.check_my_log(FUNC_KWARGS_LOG_WITH_DEFAULTS)

    def test_func_secure_list_args(self):
        func_secure_args([1, 2, 'abc'])
        self.check_my_log(FUNC_SECURE_LIST_ARGS)

    def test_func_secure_tuple_args(self):
        func_secure_args((1, 2, 'abc'))
        self.check_my_log(FUNC_SECURE_TUPLE_ARGS)

    def test_func_secure_dict_args(self):
        func_secure_args({'key1': 'value'})
        self.check_my_log(FUNC_SECURE_DICT_ARGS)

    def test_func_return_obj(self):
        func_return_obj()
        self.check_my_log(FUNC_LOG_RETURN_OBJ)

    def test_simple_info(self):
        logger.info("Just some info message.")
        self.check_my_log(INFO_LOG)

    def test_info_with_args(self):

        logger.info({
            'MESSAGE': "This log is with some arguments, that can be given for some information where you need to put "
                       "argument values.",
            'KWARGS': {
                'PARAM_OBJ': str(self),
            }
        })
        self.check_my_log(INFO_WITH_ARGS_LOG)

    def test_exception(self):
        try:
            raise Exception("Something weird happened, like running a test case ;) ")
        except Exception as e:
            logger.exception("Exception occured")

        self.check_my_log(EXCEPTION_LOG, dynamic_keys=('TRACE',))

    def test_exception_with_args(self):
        try:
            raise Exception("Something weird happened, like running a test case ;) ")
        except Exception as e:
            logger.exception({
                'MESSAGE': "Exception occurred for testing ie",
                'KWARGS': {'PARAM': None}
            })

        self.check_my_log(EXCEPTION_ARGS_LOG, dynamic_keys=('TRACE',))

    def test_warning(self):
        logger.warning("Warning occurred for the sole purpose of testing.")
        self.check_my_log(WARNING_LOG, )

    def test_warning_with_args(self):
        logger.warning({
            "MESSAGE": "Warning occurred for the sole purpose of testing.",
            "ARGS": {
                "PARAM1": "something"
            }
        })
        self.check_my_log(WARNING_LOG_WITH_ARGS, )

    def test_critical(self):
        logger.critical("Some critical !@#$%^&*() happened \'\"\' only for the sole purpose of testing.")
        self.check_my_log(CRITICAL_LOG)

    def test_critical_with_args(self):

        logger.critical({
            "MESSAGE": "Some critical !@#$%^&*() happened \'\"\' only for the sole purpose of testing.",
            "ARGS": {
                "PARAM1": "something"
            }
        })
        self.check_my_log(CRITICAL_LOG_WITH_ARGS, dynamic_keys=('TRACE',))

    def test_api_with_global_logs(self):
        client = Client()
        client.get("http://127.0.0.1:8000/test/")
        self.check_my_log(API_LOG_WITH_GLOBAL)

    def test_exception_parsing_log(self):
        logger.info({'a': object})
        self.check_my_log(EXCEPTION_WHILE_PARSING_LOG)
