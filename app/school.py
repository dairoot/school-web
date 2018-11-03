# -*- coding: utf-8 -*-
from app import redis_school
from school_api import SchoolClient
from school_api.session.redisstorage import RedisStorage
from app.utils import service_resp, random_string

session = RedisStorage(redis_school)


class School(object):

    def __init__(self, url):
        self.school_client = SchoolClient(url, session=session, use_ex_handle=False)

    @service_resp()
    def get_login(self, account, password):
        '''首次登陆验证'''
        self.user = self.school_client.user_login(account, password, use_cookie=False)
        return {"token": random_string(16)}

    @service_resp()
    def get_auth_user(self, account):
        '''使用会话，免密码登陆'''
        auth_user = self.school_client.user_login(account, None)
        return auth_user


class Client(object):
    user_client = None

    @service_resp()
    def get_schedule(self, **kwargs):
        ''' 获取课表信息 '''
        return self.user_client.get_schedule(**kwargs)

    @service_resp()
    def get_score(self, **kwargs):
        ''' 获取成绩信息 '''
        return self.user_client.get_score(**kwargs)

    @service_resp()
    def get_info(self):
        ''' 获取用户信息 '''
        return self.user_client.get_info()
