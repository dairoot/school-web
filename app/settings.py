# -*- coding: utf-8 -*-
import os
import logging.config
import logging

DSN = os.environ.get('DSN')
DEBUG = os.environ.get('DEBUG', False)

cache_time = 86400 * 7

application_settings = {
    'debug': DEBUG,
    'template_path': 'templates',
}

school_list = {
    "210.38.137.126:8016": "广东海洋大学",
    "61.142.33.204": "广东科技学院",
    "jwxt.gdyvc.cn": "广东青年职业学院",
    "jw.gzhmt.edu.cn": "广州航海学院",
    "222.24.62.120": "西安邮电大学",
    "jwgl.fjnu.edu.cn": "福建师范大学",
    "jwgl.zsc.edu.cn:90": "电子科技大学中山学院",
    "jwxt.njupt.edu.cn": "南京邮电大学",
    "202.116.160.170": "华南农业大学",
    "xjw0.fjcc.edu.cn": "福建商学院",
    "ojjx.wzu.edu.cn": "温州大学",
}

# 开发时的日志配置，INFO 及以上级别的日志输出到 console。
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
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'simple',
            'filename': 'logs/default.log',
            'maxBytes': 10 * 1024 * 1024,
            'backupCount': 5
        }
    },
    'loggers': {
        'tornado': {
            'handlers': ['console', 'default'],
            'propagate': False,
        },
    },
}

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('root')
