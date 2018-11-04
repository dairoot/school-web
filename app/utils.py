# -*- coding: utf-8 -*-
import datetime
import string
import random
from school_api.exceptions import SchoolException, LoginException, IdentityException

current_year = datetime.datetime.now().year

school_year_validate = lambda x: current_year - 4 <= int(x.split('-')[0]) < int(x.split('-')[1]) <= int(
    x.split('-')[0]) + 1 <= current_year + 1
school_term_validate = lambda x: 1 <= int(x) <= 2


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
