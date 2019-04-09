import copy
import logging

from collections import namedtuple
from .settings import logger_settings

try:
    from inspect import getfullargspec
except ImportError:
    # for python 2.7
    from inspect import getargspec as getfullargspec

logger = logging.getLogger(logger_settings.LOGGER_NAME)


def convert_to_type(type_var, var):
    return type_var(var)


class FunctionLogger(object):
    """
    Function logger to log at entry-exit of a function with arguments and output

    Usage
    -----
    @FunctionLogger(secure_args=['a','b',]
    def sum(a,b):
        return a+b

    When called as sum(1,2) it will be logged as:

    "APP":"FUNDSFLOW_IMPS","TIME":"2018-01-05T15:31:41.961+05:30","LEVEL":"INFO","LOGGER":"imps",
    "PATH":"<ipython-input-2-28c5fd5efdaf>","FUNCTION":"sum","LINE":"1",
    "IMPS_DATA":{.....},"MESSAGE":{"KWARGS": "{}", "ARGS": "NamedArgs(a='*', b='*')", "TEXT": "Entering sum"}},
    "TRACE":""}

    While initialising we can give arguments which has to be masked in secure_args list

    note:: Number of `*` has been limited to max 10, in case of exceeding length of parameter
        it will be truncated to length % 10 number of `*`
    """

    def __init__(self, secure_args=[]):
        self.secure_list = secure_args

        # read from settings if defined there
        try:
            self.secure_list += list(logger_settings.SECURE_PARAMS)
        except AttributeError:
            pass

    def _get_secure_log(self, params, arg_names=None):

        is_kwargs = False

        if type(params) == dict:
            is_kwargs = True
            _params = copy.deepcopy(params)
            secure_params = {}
        else:
            secure_params = []

        if params:
            for arg_name, var in zip(arg_names, params) if arg_names else params.items():

                arg_val = _params[arg_name] if is_kwargs else var

                if isinstance(arg_val, (list, tuple)) and arg_name in self.secure_list:

                    _ = ['*' * (len(str(i)) % 10) for i in arg_val]
                    arg_val = convert_to_type(type(arg_val), _)

                elif isinstance(arg_val, (dict,)):

                    if arg_name in self.secure_list:
                        arg_val = {k: '*' * (len(str(v)) % 10) for k, v in arg_val.items()}
                    else:
                        arg_val = {k: '*' * (len(str(v)) % 10) if k in self.secure_list else v for k, v in
                                   arg_val.items()}

                elif arg_name in self.secure_list:

                    arg_val = '*' * (len(str(arg_val)) % 10)

                if is_kwargs:
                    secure_params[arg_name] = arg_val if isinstance(arg_val, (str, dict, float, int)) else str(arg_val)
                else:
                    secure_params.append(arg_val)

        if is_kwargs:
            # Lets sort dictionary keys so that it prints alphabetically
            return secure_params
        else:
            Args = namedtuple('NamedArgs', arg_names[:len(secure_params)])
            named_secure_params = Args(*secure_params)
            return repr(named_secure_params)

    def __call__(self, fn):

        def wrapped_f(*args, **kwargs):
            log_args = args
            log_kwargs = kwargs

            arg_spec = getfullargspec(fn)

            # take only args from
            # FullArgSpec(args, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, annotations)
            arg_names = arg_spec[0]
            secure_log_args = self._get_secure_log(log_args, arg_names)
            secure_log_kwargs = self._get_secure_log(log_kwargs) if log_kwargs else ""

            logger.info({
                'MESSAGE': 'Entering {}'.format(fn.__name__),
                'ARGS': secure_log_args,
                'KWARGS': secure_log_kwargs,
                '_LNO': fn.__code__.co_firstlineno,
                '_FUNCNAME': fn.__name__,
                '_PATH': fn.__code__.co_filename
            })

            fn_output = fn(*args, **kwargs)

            secured_fn_output = copy.deepcopy(fn_output) if isinstance(fn_output, dict) else fn_output
            # Mask output only if its dict
            if isinstance(fn_output, dict):
                secured_fn_output = {
                    k: '*' * (len(str(v)) % 10) if k in self.secure_list else v for k, v in fn_output.items()
                }
            elif not isinstance(secured_fn_output, str):
                secured_fn_output = repr(secured_fn_output)

            logger.info({
                'MESSAGE': 'Exiting {}'.format(fn.__name__),
                'ARGS': secured_fn_output if secured_fn_output else "",
                '_LNO': fn.__code__.co_firstlineno,
                '_FUNCNAME': fn.__name__,
                '_PATH': fn.__code__.co_filename
            })
            return fn_output

        return wrapped_f
