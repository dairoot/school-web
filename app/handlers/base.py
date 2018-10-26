# -*- coding: utf-8 -*-
import json
from json import JSONDecodeError
from app import redis
import tornado.web
from raven.contrib.tornado import SentryMixin
from tornado.escape import json_decode
from app.school import School, Client
from app.settings import DEBUG, logger


class BaseHandler(SentryMixin, tornado.web.RequestHandler):
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
        token = self.request.headers.get("token")
        self.token_info = redis.hgetall('token:' + token)

    def prepare(self):
        if self.current_user['status_code'] == 200:
            super(AuthHandler, self).prepare()
            self.user_client = self.current_user['data']
        else:
            self.write_json(self.current_user['data'])
            return

    def get_current_user(self):
        if not self.token_info:
            return {"data": 'token无效', 'status_code': 400}
        user = School(self.token_info['url']).get_auth_user(self.token_info['account'])
        return user

