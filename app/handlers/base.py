# -*- coding: utf-8 -*-
import pickle
import json
from json import JSONDecodeError
from app import redis, redis_b
import tornado.web
from raven.contrib.tornado import SentryMixin
from tornado.escape import json_decode
from app.school import School, Client
from app.settings import DEBUG, logger, cache_time


class BaseHandler(SentryMixin, tornado.web.RequestHandler):
    result = None

    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)
        self.set_header('Content-Type', 'application/json')

    def prepare(self):
        """只处理 JSON body"""

        if self.request.body:
            try:
                json_data = json_decode(self.request.body)
            except JSONDecodeError:
                self.write_json('无效的 JSON', 400)
            else:
                # 使用 MultiDict 是为了适配 WTForms
                self.data = json_data

    def write_json(self, data, status_code=200):
        self.set_status(status_code)
        self.write(json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))
        self.finish()

    def write_error(self, status_code, **kwargs):

        if DEBUG:
            super(BaseHandler, self).write_error(status_code, **kwargs)
        else:
            logger.error(self._reason)
            # TODO


class AuthHandler(BaseHandler, Client):

    def initialize(self):
        ''' 初始化参数 '''
        token = self.request.headers.get("token")
        self.token_info = redis_b.hgetall('token:' + token)

    def prepare(self):
        if not self.token_info:
            self.write_json(data='token无效', status_code=400)
        else:
            # 获取缓存
            self.redis_key = f"{self.token_info['url']}:{self.__class__.__name__}:{self.token_info['account']}"
            self.cache_data = redis.get(self.redis_key)
            if self.cache_data:
                self.cache_data = pickle.loads(self.cache_data)
                self.time_out = redis.ttl(self.redis_key)
            super(AuthHandler, self).prepare()

    @property
    def user_client(self):
        # 请求数据
        school = School(self.token_info['url'])
        return school.get_auth_user(self.token_info['account'])['data']

    def save_cache(self, data, ttl=cache_time):
        # 缓存数据
        redis.set(self.redis_key, pickle.dumps(data), ttl)
