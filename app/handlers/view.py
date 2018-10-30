# -*- coding: utf-8 -*-
from app import redis
from app.school import School
from app.handlers.base import BaseHandler, AuthHandler
from app.settings import logger


class Login(BaseHandler):
    ''' 用户登录 '''

    async def post(self):
        self.school = School(self.data['url'])
        self.result = self.school.get_login(self.data["account"], self.data["password"])
        self.write_json(**self.result)

    def on_finish(self):
        if self.result['status_code'] == 200:
            key = f"token:{self.result['data']['token']}"
            redis.hmset(key, {"url": self.data['url'], "account": self.data["account"]})
            redis.expire(key, 24 * 3600)

            # 获取用户信息
            user_client = self.school.get_auth_user(self.data['account'])['data']
            user_info = user_client.get_info()
            logger.info("IP：%s，绑定成功：%s", self.request.remote_ip, user_info['real_name'])
            # TODO 保存用户信息
        else:
            logger.warn("IP：%s，%s", self.request.remote_ip, self.result['data'])


class Schedule(AuthHandler):
    ''' 课表获取 '''

    async def get(self):
        if self.cache_data:
            self.write_json(self.cache_data)
            # 当过期时间小于1天时，再次更新
            if self.time_out < 86400:
                result = self.get_schedule()
                self.save_cache(result['data'])
        else:
            result = self.get_schedule()
            self.write_json(**result)
            self.save_cache(result['data'])


class Score(AuthHandler):
    ''' 成绩获取 '''

    async def get(self):
        if self.cache_data:
            self.write_json(self.cache_data)
        else:
            result = self.get_score()
            self.write_json(**result)
            self.save_cache(result['data'])


class UserInfo(AuthHandler):
    ''' 用户信息获取 '''

    async def get(self):
        if self.cache_data:
            self.write_json(self.cache_data)
        else:
            result = self.get_info()
            self.write_json(**result)
            self.save_cache(result['data'])
