# -*- coding: utf-8 -*-
import pickle
from app import redis
from app.school import School
from app.handlers.base import BaseHandler, AuthHandler
from app.settings import cache_time, logger
from app.utils import school_year_validate, school_term_validate, random_string
from tornado.concurrent import run_on_executor
import tornado.gen
from schema import Schema, Optional


class Login(BaseHandler):
    ''' 用户登录 '''
    client = None
    school = None
    data_schema = Schema({
        'url': str, 'account': str, 'password': str,
        Optional('user_type', default=0): lambda x: 0 <= int(x) <= 2
    })

    @run_on_executor
    def async_login(self):
        self.school = School(self.data['url'])
        result = self.school.get_login(self.data["account"], self.data["password"], self.data['user_type'])
        if result["status_code"] == 200:
            self.client, result["data"] = result["data"], {"token": random_string()}
        return result

    @tornado.gen.coroutine
    def post(self):
        self.data['user_type'] = int(self.data['user_type'])
        self.result = yield self.async_login()
        self.write_json(**self.result)

    def on_finish(self):
        if self.result:
            base_log = f"IP：{self.request.remote_ip}，用户：{self.data['account']}"
            if self.client:
                del self.client.session
                del self.client.password
                key = f"token:{self.result['data']['token']}"
                redis.set(key, pickle.dumps(self.client, 4), 3600)
                if self.data['user_type'] != 2:
                    # 获取用户信息
                    user_info = self.client.get_info()
                    logger.info("%s，绑定成功：%s", base_log, user_info['real_name'])
                    # TODO 保存用户信息
            else:
                logger.warning("%s，错误信息：%s", base_log, self.result['data'])


class Schedule(AuthHandler):
    ''' 课表获取 '''

    data_schema = Schema({
        Optional('schedule_year', default=None): school_year_validate,
        Optional('schedule_term', default=None): school_term_validate,
        Optional('schedule_type', default=1): lambda x: 0 <= int(x) <= 1
    })

    @tornado.gen.coroutine
    def get_data(self):
        self.data["schedule_type"] = int(self.data["schedule_type"])
        if self.result:
            self.write_json(**self.result)
            # 当缓存时间已过1天，则更新数据
            if self.cache_ttl < cache_time - 86400:
                self.result = yield self.async_func(self.get_schedule, self.data)
                self.save_cache(cache_time)
        else:
            self.result = yield self.async_func(self.get_schedule, self.data)
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
        Optional('score_year', default=None): school_year_validate,
        Optional('score_term', default=None): school_term_validate,
        Optional('use_api', default=0): lambda x: 0 <= int(x) <= 2
    })

    def score_result(self):
        score_year = self.data['score_year']
        score_term = self.data['score_term']
        data = {}
        data.update(self.result)
        if score_year and data['status_code'] == 200:
            if score_term:
                data['data'] = data['data'].get(score_year, {}).get(str(score_term))
                return data
            data['data'] = data['data'].get(score_year)
            return data
        return data

    @tornado.gen.coroutine
    def get_data(self):
        if self.result:
            score_data = self.score_result()
            self.write_json(**score_data)
        else:
            data = {"use_api": int(self.data["use_api"])}
            self.result = yield self.async_func(self.get_score, data)
            score_data = self.score_result()
            self.write_json(**score_data)
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
    def get_data(self):
        if self.result:
            self.write_json(**self.result)
        else:
            self.result = yield self.async_func(self.get_info)
            self.write_json(**self.result)
            self.save_cache()

    @tornado.gen.coroutine
    def get(self):
        yield self.get_data()

    @tornado.gen.coroutine
    def post(self):
        yield self.get_data()
