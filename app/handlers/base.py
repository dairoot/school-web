# -*- coding: utf-8 -*-
import json
import pickle
from concurrent.futures import ThreadPoolExecutor
from raven.contrib.tornado import SentryMixin
from app import redis
from app.school import Client
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
            except json.JSONDecodeError:
                self.write_json('无效的 JSON', 400)
            else:
                self.data = json_data

        try:
            self.data = self.data_schema.validate(self.data)
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
        self.token_info = redis.get(f'token:{token}')

    def prepare(self):
        if not self.token_info:
            self.write_json(data='token无效', status_code=400)
        else:
            self.client = pickle.loads(self.token_info)
            super(AuthHandler, self).prepare()

            # 获取缓存
            self.redis_key = f"{self.client.base_url}:{self.__class__.__name__}:{self.client.account}"
            if self.__class__.__name__ == "Schedule":
                self.redis_key = f"{self.redis_key}:{self.data}"
            self.cache_data = redis.get(self.redis_key)
            if self.cache_data:
                self.result = {'data': pickle.loads(self.cache_data), 'status_code': 200}
                self.cache_ttl = redis.ttl(self.redis_key)

    def save_cache(self, ttl=cache_time):
        # 缓存数据
        if self.result['status_code'] == 200:
            redis.set(self.redis_key, pickle.dumps(self.result['data']), ttl)

    @run_on_executor
    def async_func(self, func, data=None):
        data = data or {}
        return func(**data)

    def on_finish(self):
        if self.token_info:
            if self.result:
                base_log = f"IP：{self.request.remote_ip}，用户：{self.client.account}"
                if self.result['status_code'] == 200:
                    logger.info("%s 进行%s操作", base_log, self.__class__.__name__)
                else:
                    logger.warning("%s，%s", base_log, self.result['data'])
        else:
            logger.warning("无效token：%s", self.request.headers.get("token"))
