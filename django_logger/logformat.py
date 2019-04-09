BASE_LOGGING_FORMAT = {
    'version': 1,
    'disable_existing_loggers': False,

    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },

    'formatters': {

        'simple': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },

        'detailed_log_track': {
            'format': '''
                        {
                            "APP": "$PATH_APP_NAME",
                            "TIME": "%(time)s",
                            "LEVEL": "%(levelname)s",
                            "LOGGER": "%(name)s",
                            "PATH": "%(pathname)s",
                            "FUNCTION": "%(funcName)s",
                            "LINE": "%(lineno)d",
                            "TRACE": "%(trace)s"
                        }''',  # .replace('$PATH_APP',logger_settings.APP),

            # 'datefmt': '%Y-%m-%d %H:%M:%S',

        },
    },
    'handlers': {

        'console': {
            'level': 'INFO',
            'class': 'django_logger.log_handler.ContextHandler',
            'formatter': 'detailed_log_track'

        },
        'mail_admins': {
            'level': 'INFO',
            # we don't want to send you mails while in dev mode
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'detailed_log_track',

        },

    },

    'loggers': {
        "$PATH_LOGGER_NAME": {
            'handlers': ['console', ],
            'propagate': False,
            'level': 'INFO',
        },
        # Mail logger should log message to console as well.
        "$PATH_MAIL_LOGGER_NAME": {
            'handlers': ['console', 'mail_admins', ],
            'propagate': False,
            'level': 'INFO',
        },
    },
}