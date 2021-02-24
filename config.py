import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # REST
    REST_URL_PREFIX = '/api/v1'
    # Redshift
    RS_USR = os.environ.get('RS_USR', 'awsuser')
    RS_PWD = os.environ.get('RS_PWD', 'password')
    RS_HOST = os.environ.get('RS_HOST', '127.0.0.1')
    RS_PORT = os.environ.get('RS_PORT', '5439')
    RS_DB = os.environ.get('RS_DB', 'prod')
    RS_IAM_ROLE = os.environ.get('RS_IAM_ROLE', 'DEFAULT_ROLE')
    S3_BUCKET = os.environ.get('S3_BUCKET', 'S3_BUCKET_ID')
    S3_REGION = os.environ.get('S3_REGION', 'S3_REGION_ID')
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
    RS_DB = os.environ.get('RS_DB_TEST', 'dev')
