# -*- coding: utf-8 -*-
import tornado.httpserver
import tornado.ioloop
import tornado.template
import tornado.web
from raven.contrib.tornado import AsyncSentryClient
from tornado.options import define, options, parse_command_line

from app import settings
from app.urls import url_patterns

define("port", default=8888, help="port", type=int)


class CustomApplication(tornado.web.Application):
    def __init__(self):
        tornado.web.Application.__init__(self, url_patterns, **settings.application_settings)
        self.sentry_client = AsyncSentryClient(settings.DSN)


def make_app():
    return CustomApplication()


def main():
    parse_command_line()
    app = make_app()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
