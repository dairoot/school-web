# -*- coding: utf-8 -*-
from app.school import School
from app.handlers.base import BaseHandler, AuthHandler
from app.settings import cache_time
from app import redis
from app.settings import logger
from tornado.concurrent import run_on_executor
import tornado.gen
from schema import Schema, Optional


class Login(BaseHandler):
    ''' 用户登录 '''
    school = None
    data_schema = Schema({'url': str, 'account': str, 'password': str})

    @run_on_executor
    def async_login(self):
        self.school = School(self.data['url'])
        return self.school.get_login(self.data["account"], self.data["password"])

    @tornado.gen.coroutine
    def post(self):
        self.result = yield self.async_login()
        self.write_json(**self.result)

    def on_finish(self):
        base_log = f"IP：{self.request.remote_ip}，用户：{self.data['account']}"
        if self.result:
            if self.result['status_code'] == 200:
                key = f"token:{self.result['data']['token']}"
                redis.hmset(key, {"url": self.data['url'], "account": self.data["account"]})
                redis.expire(key, 3600)

                # 获取用户信息
                user_client = self.school.get_auth_user(self.data['account'])['data']
                user_info = user_client.get_info()
                logger.info("%s，绑定成功：%s", base_log, user_info['real_name'])
                # TODO 保存用户信息
            else:
                logger.warning("%s，错误信息：%s", base_log, self.result['data'])


class Schedule(AuthHandler):
    ''' 课表获取 '''
    data_schema = Schema({
        Optional('schedule_year', default=None): str,
        Optional('schedule_term', default=None): str,
        Optional('schedule_type', default=0): int
    })

    @tornado.gen.coroutine
    def get_data(self):
        if self.result:
            self.write_json(**self.result)
            # 当缓存时间已过1天，则更新数据
            if self.cache_ttl < cache_time - 86400:
                self.result = yield self.async_func(self.get_schedule)
                self.save_cache(cache_time)
        else:
            self.result = yield self.async_func(self.get_schedule)
            self.write_json(**self.result)
            self.save_cache(cache_time)

    @tornado.gen.coroutine
    def get(self):
        yield self.get_data()

    @tornado.gen.coroutine
    def post(self):
        yield self.get_data()


class Score(AuthHandler):
    ''' 成绩获取 '''
    data_schema = Schema({
        Optional('score_year', default=None): str,
        Optional('score_term', default=None): str,
        Optional('use_api', default=0): int
    })

    @tornado.gen.coroutine
    def get_data(self):
        if self.result:
            self.write_json(**self.result)
        else:
            self.result = yield self.async_func(self.get_score)
            self.write_json(**self.result)
            self.save_cache()

    @tornado.gen.coroutine
    def get(self):
        yield self.get_data()

    @tornado.gen.coroutine
    def post(self):
        yield self.get_data()


class UserInfo(AuthHandler):
    ''' 用户信息获取 '''

    @tornado.gen.coroutine
    def get(self):
        if self.result:
            self.write_json(**self.result)
        else:
            self.result = yield self.async_func(self.get_info)
            self.write_json(**self.result)
            self.save_cache()
