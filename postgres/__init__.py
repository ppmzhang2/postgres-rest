import os

import config

env = os.getenv('ENV', 'test')

if env == 'prod':
    cfg = config.Config
elif env == 'test':
    cfg = config.TestConfig
else:
    raise ValueError('Invalid environment name')
