# -*- coding: utf-8 -*-
from app import redis
from app.school import School
from app.handlers.base import BaseHandler, AuthHandler


class Login(BaseHandler):
    ''' 用户登录 '''

    async def post(self):
        url = self.data.pop('url')
        result = School(url).get_login(**self.data)
        self.write_json(**result)

        if result['status_code'] == 200:
            key = f"token:{result['data']['token']}"
            redis.hmset(key, {"url": url, "account": self.data['account']})
            redis.expire(key, 24 * 3600)


class Schedule(AuthHandler):
    ''' 课表获取 '''

    async def get(self):
        if self.cache_data:
            self.write_json(self.cache_data)
            # 当过期时间小于1天时，再次更新
            if self.time_out < 86400:
                self.result = self.get_schedule()
                self.save_cache(self.result)
        else:
            self.result = self.get_schedule()
            self.write_json(**self.result)
            self.save_cache(self.result)


class Score(AuthHandler):
    ''' 成绩获取 '''

    async def get(self):
        if self.cache_data:
            self.write_json(self.cache_data)
        else:
            self.result = self.get_score()
            self.write_json(**self.result)
            self.save_cache(self.result, ttl=86400 * 7)


class UserInfo(AuthHandler):
    ''' 用户信息获取 '''

    async def get(self):
        if self.cache_data:
            self.write_json(self.cache_data)
        else:
            self.result = self.get_info()
            self.write_json(**self.result)
            self.save_cache(self.result, ttl=86400 * 7)
