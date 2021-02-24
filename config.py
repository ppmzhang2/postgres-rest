import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # REST
    REST_URL_PREFIX = '/api/v1'
    # SqlAlchemy
    SA_HOST = os.environ.get('SA_HOST', 'localhost')
    SA_PORT = os.environ.get('SA_PORT', 5432)
    SA_DB = os.environ.get('SA_DB_PROD', 'prod')
    SA_USR = os.environ.get('SA_USR', 'YOUR_USERNAME')
    SA_PWD = os.environ.get('SA_PWD', 'YOUR_PASSWORD')
    # Logging
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'nano': {
                'format': '%(asctime)s  %(message)s'
            },
            'micro': {
                'format':
                '%(asctime)s [%(levelname)s] '
                '%(name)s: '
                '%(message)s',
            },
            'small': {
                'format':
                '%(asctime)s [%(levelname)s] '
                '%(real_module)s - %(real_funcName)s - %(real_lineno)s: '
                '%(message)s',
            },
        },
        'handlers': {
            'info_file': {
                'level': 'INFO',
                'formatter': 'small',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'when': 'H',
                'interval': 1,
                'backupCount': 6,
                'filename': f'{basedir}/logs/rest/info.log',
            },
            'debug_streamer': {
                'level': 'DEBUG',
                'formatter': 'small',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',
            },
            'debug_file': {
                'level': 'DEBUG',
                'formatter': 'small',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'when': 'M',
                'interval': 1,
                'backupCount': 30,
                'filename': f'{basedir}/logs/rest/debug.log',
            },
        },
        'loggers': {
            'info_logger': {
                'handlers': ['debug_file', 'info_file'],
                'level': 'DEBUG',
                'propagate': False,
            },
        },
    }


class TestConfig(Config):
    SA_DB = os.environ.get('SA_DB_TEST', 'test')
