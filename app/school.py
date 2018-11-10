# -*- coding: utf-8 -*-
from app import redis
from school_api import SchoolClient
from school_api.session.redisstorage import RedisStorage
from app.utils import service_resp

session = RedisStorage(redis)


class School(object):

    def __init__(self, url):
        self.school_client = SchoolClient(url, session=session, use_ex_handle=False)

    @service_resp()
    def get_login(self, account, password, user_type=0):
        '''首次登陆验证'''
        return self.school_client.user_login(account, password, user_type=user_type, use_cookie=False)


class Client(object):
    client = None

    @service_resp()
    def get_schedule(self, **kwargs):
        ''' 获取课表信息 '''
        return self.client.get_schedule(**kwargs)

    @service_resp()
    def get_score(self, **kwargs):
        ''' 获取成绩信息 '''
        return self.client.get_score(**kwargs)

    @service_resp()
    def get_info(self):
        ''' 获取用户信息 '''
        return self.client.get_info()
