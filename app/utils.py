# -*- coding: utf-8 -*-
import pickle
import string
import random
from app import redis
from school_api.exceptions import SchoolException, LoginException, IdentityException


def random_string(length=16):
    rule = string.ascii_letters + string.digits
    rand_list = random.sample(rule, length)
    return ''.join(rand_list)


# 异常处理装饰器
def service_resp():
    def decorator(func):
        def warpper(*args, **kwargs):
            try:
                data = func(*args, **kwargs)
            except IdentityException as reqe:
                return {'data': str(reqe), 'status_code': 400}
            except LoginException as reqe:
                return {'data': str(reqe), 'status_code': 400}
            except SchoolException as reqe:
                return {'data': str(reqe), 'status_code': 400}
            else:
                return {'data': data, 'status_code': 200}

        return warpper

    return decorator
