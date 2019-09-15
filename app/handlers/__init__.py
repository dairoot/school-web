# -*- coding: utf-8 -*-
import json
import datetime
import feedparser
from tornado.web import RequestHandler
from app.settings import school_list


class SchoolList(RequestHandler):

    def get(self):
        school_list.sort(key=lambda k: (k.get('code', 0)))
        self.write(json.dumps(school_list))
        self.finish()


class Index(RequestHandler):

    def get(self):
        with open('./templates/index.html', 'rb') as f:
            self.write(f.read())
            self.finish()


class Rss(RequestHandler):

    def get(self):
        fp = feedparser.parse('https://blog.dairoot.cn/atom.xml')
        article = []
        for e in fp.entries:
            article.append({
                'tag': e.category,
                'title': e.title,
                'date': e.published.split("T")[0],
                'url': e.links[0].href,
                'content': e.content[0].value
            })
        self.write(json.dumps(article))
        self.finish()
