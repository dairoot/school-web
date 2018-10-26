# -*- coding: utf-8 -*-
from app import redis
from app.school import School
from app.handlers.base import BaseHandler, AuthHandler


class Login(BaseHandler):

    async def post(self):
        url = self.data.pop('url')
        result = School(url).get_login(**self.data)
        self.write_json(**result)

        if result['status_code'] == 200:
            key = f"token:{result['data']['token']}"
            redis.hmset(key, {"url": url, "account": self.data['account']})
            redis.expire(key, 24 * 3600)


class Schedule(AuthHandler):

    async def get(self):
        data = self.get_schedule()
        self.write_json(**data)


class Score(AuthHandler):

    async def get(self):
        data = self.get_score()
        self.write_json(**data)


class UserInfo(AuthHandler):

    async def get(self):
        data = self.get_info()
        self.write_json(**data)
