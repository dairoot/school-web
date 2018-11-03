# -*- coding: utf-8 -*-
from app.school import School
from app.handlers.base import BaseHandler, AuthHandler
from app.settings import cache_time
from tornado.concurrent import run_on_executor
import tornado.gen

class Login(BaseHandler):
    ''' 用户登录 '''

    @run_on_executor
    def async_login(self):
        self.school = School(self.data['url'])
        return  self.school.get_login(self.data["account"], self.data["password"])

    @tornado.gen.coroutine
    def post(self):
        self.result = yield self.async_login()
        self.write_json(**self.result)


class Schedule(AuthHandler):
    ''' 课表获取 '''

    @tornado.gen.coroutine
    def get(self):
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


class Score(AuthHandler):
    ''' 成绩获取 '''

    @tornado.gen.coroutine
    def get(self):
        if self.result:
            self.write_json(**self.result)
        else:
            self.result = yield self.async_func(self.get_score)
            self.write_json(**self.result)
            self.save_cache()


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
