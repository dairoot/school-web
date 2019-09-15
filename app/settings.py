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
    'static_path': 'static',

}

school_list = [
    {"url": "http://jwgl.zsc.edu.cn:90/", "name": "电子科技大学中山学院", "code": "dianzikejidaxuezhongshanxueyuan"},
    {"url": "http://210.38.137.126:8016/", "name": "广东海洋大学", "code": "guangdonghaiyangdaxue"},
    {"url": "http://61.142.33.204/", "name": "广东科技学院", "code": "guangdongkejixueyuan"},
    {"url": "http://jwxt.gdyvc.cn/", "name": "广东青年职业学院", "code": "guangdongqingnianzhiyexueyuan"},
    {"url": "http://jw.gzhmt.edu.cn/", "name": "广州航海学院", "code": "guagnzhouhanghaixueyuan"},
    {"url": "http://222.24.62.120/", "name": "西安邮电大学", "code": "xianyoudiandaxue"},
    {"url": "http://jwgl.fjnu.edu.cn/", "name": "福建师范大学", "code": "fujianshifandaxue"},
    {"url": "http://jwxt.njupt.edu.cn/", "name": "南京邮电大学", "code": "nanjingyoudiandaxue"},
    {"url": "http://202.116.160.170/", "name": "华南农业大学", "code": "huanannongyedaxue"},
    {"url": "http://xjw0.fjcc.edu.cn/", "name": "福建商学院", "code": "fujianshangxueyuan"},
    {"url": "http://ojjx.wzu.edu.cn/", "name": "温州大学", "code": "wenzhoudaxue"},
    {"url": "http://125.221.35.100/", "name": "武汉软件工程职业学院", "code": "wuhanruanjiangongchengzhiyexueyuan"},
    {"url": "http://jwxt.gcu.edu.cn/", "name": "华南理工大学广州学院", "code": "huananligongdaxueguangzhouxueyuan"},
    {"url": "http://202.200.112.200/", "name": "西安理工大学", "code": "xianligongdaxue"},
    {"url": "http://210.37.0.22/", "name": "海南师范大学", "code": "hainanshifandaxue"}
]

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
