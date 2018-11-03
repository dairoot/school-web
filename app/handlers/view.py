# -*- coding: utf-8 -*-
from app import redis
from app.school import School
from app.handlers.base import BaseHandler, AuthHandler
from app.settings import logger, cache_time


class Login(BaseHandler):
    ''' 用户登录 '''

    async def post(self):

        self.school = School(self.data['url'])
        self.result = self.school.get_login(self.data["account"], self.data["password"])
        self.write_json(**self.result)

    def on_finish(self):
        base_log = f"IP：{self.request.remote_ip}，用户：{self.data['account']}"
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
            logger.warn("%s，错误信息：%s", base_log, self.result['data'])


class Schedule(AuthHandler):
    ''' 课表获取 '''

    async def get(self):
        if self.result:
            self.write_json(**self.result)
            # 当缓存时间已过1天，则更新数据
            if self.time_out < cache_time - 86400:
                self.result = self.get_schedule()
                self.save_cache(cache_time)
        else:
            self.result = self.get_schedule()
            self.write_json(**self.result)
            self.save_cache(cache_time)


class Score(AuthHandler):
    ''' 成绩获取 '''

    async def get(self):
        if self.result:
            self.write_json(**self.result)
        else:
            self.result = self.get_score()
            self.write_json(**self.result)
            self.save_cache()


class UserInfo(AuthHandler):
    ''' 用户信息获取 '''

    async def get(self):

        if self.result:
            self.write_json(**self.result)
        else:
            self.result = self.get_info()
            self.write_json(**self.result)
            self.save_cache()
