# -*- coding: utf-8 -*-
from tornado.web import RequestHandler
from app.settings import school_list


class Index(RequestHandler):

    def get(self):
        self.render('index.html', school_list=school_list)
