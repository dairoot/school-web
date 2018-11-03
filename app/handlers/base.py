# -*- coding: utf-8 -*-
import json
import pickle
from json import JSONDecodeError
from concurrent.futures import ThreadPoolExecutor
from raven.contrib.tornado import SentryMixin
from app import redis_school, redis

from app.school import School, Client
from app.settings import DEBUG, logger, cache_time

from tornado.web import RequestHandler
from tornado.escape import json_decode
from tornado.concurrent import run_on_executor
from schema import SchemaError, Schema

class BaseHandler(SentryMixin, RequestHandler):
    result = None
    data = {}
    data_schema = Schema({})
    executor = ThreadPoolExecutor(5)

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
                self.data = json_data

        try:
            self.data_schema.validate(self.data)
        except SchemaError as emsg:
            self.write_json(str(emsg), 400)

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
    token_info = None
    cache_ttl = None
    redis_key = None
    cache_data = None

    def initialize(self):
        ''' 初始化参数 '''
        token = self.request.headers.get("token")
        self.token_info = redis.hgetall('token:' + token)

    def prepare(self):
        if not self.token_info:
            self.write_json(data='token无效', status_code=400)
        else:
            # 获取缓存
            self.redis_key = f"{self.token_info['url']}:{self.__class__.__name__}:{self.token_info['account']}"
            self.cache_data = redis_school.get(self.redis_key)
            if self.cache_data:
                self.result = {'data': pickle.loads(self.cache_data), 'status_code': 200}
                self.cache_ttl = redis_school.ttl(self.redis_key)
            super(AuthHandler, self).prepare()

    @property
    def user_client(self):
        # 返回请求对象
        school = School(self.token_info['url'])
        return school.get_auth_user(self.token_info['account'])['data']

    def save_cache(self, ttl=cache_time):
        # 缓存数据
        if self.result['status_code'] == 200:
            redis_school.set(self.redis_key, pickle.dumps(self.result['data']), ttl)

    @run_on_executor
    def async_func(self, func):
        return func(**self.data)

    def on_finish(self):
        if self.token_info:
            base_log = f"IP：{self.request.remote_ip}，用户：{self.token_info['account']}"
            if self.result['status_code'] == 200:
                logger.info("%s 进行%s操作", base_log, self.__class__.__name__)
            else:
                logger.warning("%s，%s", base_log, self.result['data'])
        else:
            logger.warning("无效token：%s", self.request.headers.get("token"))
