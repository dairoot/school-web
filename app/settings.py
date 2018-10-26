# -*- coding: utf-8 -*-
import os
import logging.config
import logging

DEBUG = os.environ.get('DEBUG', False)

application_settings = {
    'debug': DEBUG,
}

DSN = ''

# 开发时的日志配置，INFO 及以上级别的日志输出到 console。生产环境的配置见 xiangliu-deployment
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'handlers': ['console'],
    },
    'formatters': {
        'simple': {
            'format': '[%(asctime)s] %(levelname)s [%(module)s|%(lineno)s] - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'tornado': {
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('root')
