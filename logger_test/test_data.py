FUNC_BLANK_LOG = ({"LEVEL": "INFO", "TEST_MY_DATA": {"FLOAT": 0.00, "f": {"b": 0, "a": "", "c": {"c": "{}"}}, "INT": 0,
                                                     "MESSAGE": {"TEXT": "Entering func_blank", "ARGS": "NamedArgs()",
                                                                 "KWARGS": ""}, "C": ""}, "APP": "test",

                   "LOGGER": "test", "TRACE": "", "FUNCTION": "func_blank"},
                  {"LEVEL": "INFO", "TEST_MY_DATA": {"FLOAT": 0.00, "f": {"b": 0, "a": "", "c": {"c": "{}"}}, "INT": 0,
                                                     "MESSAGE": {"TEXT": "Exiting func_blank", "ARGS": "Any Value",
                                                                 "KWARGS": ""}, "C": ""}, "APP": "test",

                   "LOGGER": "test", "TRACE": "", "FUNCTION": "func_blank"}
                  )

FUNC_ARGS_LOG = (
    {"TRACE": "", "FUNCTION": "func_args",
     "LOGGER": "test",
     "TEST_MY_DATA": {"f": {"c": {"c": "{}"}, "b": 0, "a": ""}, "C": "", "INT": 0, "FLOAT": 0.00,
                      "MESSAGE": {"ARGS": "NamedArgs(username='***', password='***')",
                                  "TEXT": "Entering func_args", "KWARGS": ""}}, "APP": "test", "LEVEL": "INFO"},
    {"TRACE": "", "FUNCTION": "func_args",
     "LOGGER": "test", "TEST_MY_DATA": {"f": {"c": {"c": "{}"}, "b": 0, "a": ""}, "C": "", "INT": 0, "FLOAT": 0.00,
                                        "MESSAGE": {"ARGS": "Username - test_password", "TEXT": "Exiting func_args",
                                                    "KWARGS": ""}},
     "APP": "test", "LEVEL": "INFO"}
)

FUNC_KWARGS_LOG_WITH_VALUES = (
    {"FUNCTION": "func_kwargs", "APP": "test", "TRACE": "", "TEST_MY_DATA": {"INT": 0, "MESSAGE": {
        "TEXT": "Entering func_kwargs", "KWARGS": "{'arg1': 10}",
        "ARGS": "NamedArgs(username='test_username')"}, "C": "", "f": {"b": 0, "a": "", "c": {"c": "{}"}},
                                                                             "FLOAT": 0.00},
     "LOGGER": "test", "LEVEL": "INFO"},
    {"FUNCTION": "func_kwargs", "APP": "test", "TRACE": "", "TEST_MY_DATA": {"INT": 0, "MESSAGE": {
        "TEXT": "Exiting func_kwargs", "KWARGS": "", "ARGS": "username10"}, "C": "",
                                                                             "f": {"b": 0, "a": "",
                                                                                   "c": {"c": "{}"}},
                                                                             "FLOAT": 0.00},
     "LOGGER": "test", "LEVEL": "INFO"}
)

FUNC_KWARGS_LOG_WITH_DEFAULTS = (
    {"FUNCTION": "func_kwargs", "APP": "test", "TRACE": "", "TEST_MY_DATA": {"INT": 0, "MESSAGE": {
        "TEXT": "Entering func_kwargs", "KWARGS": "",
        "ARGS": "NamedArgs(username='test_username')"}, "C": "", "f": {"b": 0, "a": "", "c": {"c": "{}"}},
                                                                             "FLOAT": 0.00},
     "LOGGER": "test", "LEVEL": "INFO"},
    {"FUNCTION": "func_kwargs", "APP": "test", "TRACE": "", "TEST_MY_DATA": {"INT": 0, "MESSAGE": {
        "TEXT": "Exiting func_kwargs", "KWARGS": "", "ARGS": "username3"}, "C": "",
                                                                             "f": {"b": 0, "a": "",
                                                                                   "c": {"c": "{}"}},
                                                                             "FLOAT": 0.00},
     "LOGGER": "test", "LEVEL": "INFO"}
)

FUNC_SECURE_LIST_ARGS = ({"TEST_MY_DATA": {"C": "", "INT": 0, "FLOAT": 0.00,
                                           "MESSAGE": {"ARGS": "NamedArgs(secure_arg=['*', '*', '***'])",
                                                       "TEXT": "Entering func_secure_args", "KWARGS": ""},
                                           "f": {"a": "", "c": {"c": "{}"}, "b": 0}}, "LEVEL": "INFO", "LOGGER": "test",
                          "FUNCTION": "func_secure_args", "APP": "test", "TRACE": ""}
                         , {"TEST_MY_DATA": {"C": "", "INT": 0, "FLOAT": 0.00,
                                             "MESSAGE": {"ARGS": "{'secure_arg': '***'}",
                                                         "TEXT": "Exiting func_secure_args", "KWARGS": ""},
                                             "f": {"a": "", "c": {"c": "{}"}, "b": 0}}, "LEVEL": "INFO",
                            "LOGGER": "test", "FUNCTION": "func_secure_args", "APP": "test", "TRACE": ""}
                         )

FUNC_SECURE_TUPLE_ARGS = ({"TEST_MY_DATA": {"C": "", "INT": 0, "FLOAT": 0.00,
                                            "MESSAGE": {"ARGS": "NamedArgs(secure_arg=('*', '*', '***'))",
                                                        "TEXT": "Entering func_secure_args", "KWARGS": ""},
                                            "f": {"a": "", "c": {"c": "{}"}, "b": 0}}, "LEVEL": "INFO",
                           "LOGGER": "test",
                           "FUNCTION": "func_secure_args", "APP": "test", "TRACE": ""}
                          , {"TEST_MY_DATA": {"C": "", "INT": 0, "FLOAT": 0.00,
                                              "MESSAGE": {"ARGS": "{'secure_arg': '***'}",
                                                          "TEXT": "Exiting func_secure_args", "KWARGS": ""},
                                              "f": {"a": "", "c": {"c": "{}"}, "b": 0}}, "LEVEL": "INFO",
                             "LOGGER": "test", "FUNCTION": "func_secure_args", "APP": "test", "TRACE": ""}
                          )

FUNC_SECURE_DICT_ARGS = ({"TEST_MY_DATA": {"C": "", "INT": 0, "FLOAT": 0.00,
                                           "MESSAGE": {"ARGS": "NamedArgs(secure_arg={'key1': '*****'})",
                                                       "TEXT": "Entering func_secure_args", "KWARGS": ""},
                                           "f": {"a": "", "c": {"c": "{}"}, "b": 0}}, "LEVEL": "INFO", "LOGGER": "test",
                          "FUNCTION": "func_secure_args", "APP": "test", "TRACE": ""}
                         , {"TEST_MY_DATA": {"C": "", "INT": 0, "FLOAT": 0.00,
                                             "MESSAGE": {"ARGS": "{'secure_arg': '***'}",
                                                         "TEXT": "Exiting func_secure_args", "KWARGS": ""},
                                             "f": {"a": "", "c": {"c": "{}"}, "b": 0}}, "LEVEL": "INFO",
                            "LOGGER": "test", "FUNCTION": "func_secure_args", "APP": "test", "TRACE": ""}
                         )

FUNC_LOG_RETURN_OBJ = ({"APP": "test", "LEVEL": "INFO", "LOGGER": "test", "FUNCTION": "func_return_obj", "TRACE": "",
                        "TEST_MY_DATA": {"INT": 0, "FLOAT": 0.00, "C": "", "f": {"a": "", "b": 0, "c": {"c": "{}"}},
                                         "MESSAGE": {"TEXT": "Entering func_return_obj", "ARGS": "NamedArgs()",
                                                     "KWARGS": ""}}},
                       {"APP": "test", "LEVEL": "INFO", "LOGGER": "test", "FUNCTION": "func_return_obj", "TRACE": "",
                        "TEST_MY_DATA": {"INT": 0, "FLOAT": 0.00, "C": "", "f": {"a": "", "b": 0, "c": {"c": "{}"}},
                                         "MESSAGE": {"TEXT": "Exiting func_return_obj", "ARGS": "<type 'int'>",
                                                     "KWARGS": ""}}}
                       )

INFO_LOG = ({"FUNCTION": "test_simple_info", "LEVEL": "INFO", "LOGGER": "test",
             "TEST_MY_DATA": {"C": "", "f": {"b": 0, "c": {"c": "{}"}, "a": ""}, "FLOAT": 0.00,
                              "MESSAGE": {"TEXT": "Just some info message."}, "INT": 0}, "APP": "test",
             "TRACE": ""},)

INFO_WITH_ARGS_LOG = ({"LOGGER": "test", "TRACE": "",
                       "TEST_MY_DATA": {"C": "", "FLOAT": 0.00, "f": {"b": 0, "c": {"c": "{}"}, "a": ""}, "INT": 0,
                                        "MESSAGE": {
                                            "ARGS": "",
                                            "TEXT": "This log is with some arguments, that can be "
                                                    "given for some information where you need to put "
                                                    "argument values.",
                                            "KWARGS": "{'PARAM_OBJ': 'test_info_with_args (tests.TestDjangoLogger)'}"}},
                       "FUNCTION": "test_info_with_args", "APP": "test", "LEVEL": "INFO"}
                      ,)

EXCEPTION_LOG = (
    {"LOGGER": "test", "FUNCTION": "test_exception", "LEVEL": "ERROR",
     "APP": "test",
     "TEST_MY_DATA": {"MESSAGE": {"TEXT": "Exception occured"},
                      "f": {"a": "", "b": 0, "c": {"c": "{}"}}, "FLOAT": 0.00,
                      "INT": 0, "C": ""}},)

EXCEPTION_ARGS_LOG = ({"LEVEL": "ERROR", "APP": "test", "FUNCTION": "test_exception_with_args",
                       "LOGGER": "test",
                       "TEST_MY_DATA": {"C": "", "INT": 0,
                                        "FLOAT": 0.00,
                                        "f": {"b": 0, "a": "", "c": {"c": "{}"}},
                                        "MESSAGE": {"KWARGS": "{'PARAM': None}", "ARGS": "",
                                                    "TEXT": "Exception occurred for testing ie"}},
                       }
                      ,)

WARNING_LOG = ({"LOGGER": "test", "APP": "test", "LEVEL": "WARNING",
                "TEST_MY_DATA": {"MESSAGE": {"TEXT": "Warning occurred for the sole purpose of testing."},
                                 "FLOAT": 0.00, "INT": 0, "f": {"b": 0, "a": "", "c": {"c": "{}"}}, "C": ""},
                "TRACE": "", "FUNCTION": "test_warning"},
               )

WARNING_LOG_WITH_ARGS = (
    {"TRACE": "", "FUNCTION": "test_warning_with_args", "APP": "test",
     "TEST_MY_DATA": {
         "MESSAGE": {"TEXT": "Warning occurred for the sole purpose of testing.", "ARGS": "{'PARAM1': "
                                                                                          "'something'}",
                     "KWARGS": ""}, "C": "", "f": {"b": 0, "a": "", "c": {"c": "{}"}}, "FLOAT": 0.00, "INT": 0},
     "LOGGER": "test",
     "LEVEL": "WARNING"},)

CRITICAL_LOG = ({"LOGGER": "test", "LEVEL": "CRITICAL", "APP": "test", "TEST_MY_DATA": {"INT": 0, "MESSAGE": {
    "TEXT": "Some critical !@#$%^&*() happened '\"' only for the sole purpose of testing."},
                                                                                        "f": {"c": {"c": "{}"}, "b": 0,
                                                                                              "a": ""},
                                                                                        "FLOAT": 0.00, "C": ""},
                 "TRACE": "None", "FUNCTION": "test_critical"},
                )

CRITICAL_LOG_WITH_ARGS = (
    {"TRACE": "None", "FUNCTION": "test_critical_with_args", "LEVEL": "CRITICAL", "LOGGER": "test",
     "APP": "test",
     "TEST_MY_DATA": {"FLOAT": 0.00, "C": "", "INT": 0, "f": {"c": {"c": "{}"}, "b": 0, "a": ""},
                      "MESSAGE": {"ARGS": "{'PARAM1': 'something'}", "KWARGS": "",
                                  "TEXT": "Some critical !@#$%^&*() happened '\"' only for the sole purpose "
                                          "of testing."}}}
    ,)

API_LOG_WITH_GLOBAL = (
    {"TRACE": "", "LOGGER": "test", "LEVEL": "INFO",
     "TEST_MY_DATA": {"C": "something else", "f": {"a": "some text", "b": 0,
                                                   "c": {"c": "{'x': <type 'object'>}"}
                                                   }, "INT": 10, "FLOAT": 9.32, "MESSAGE": {
         "TEXT": "Just to test global logs."}}, "APP": "test", "FUNCTION": "get"}
    ,)

EXCEPTION_WHILE_PARSING_LOG = (
    {"LEVEL": "INFO", "FUNCTION": "test_exception_parsing_log", "TRACE": "", "LOGGER": "test",
     "TEST_MY_DATA": {"INT": 0, "FLOAT": 0.00, "f": {"c": {"c": "{}"}, "b": 0, "a": ""},
                      "MESSAGE": {
                          "ERROR": "Exception occurred while parsing `invalid syntax ("
                                   "<unknown>, line 1)`",
                          "MESSAGE": "{\"OBJ\": \"{'a': <type 'object'>}\"}"}, "C": ""},
     "APP": "test", }
    ,)
