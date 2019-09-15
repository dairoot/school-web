# -*- coding: utf-8 -*-
from app.handlers import Index, SchoolList, Rss
from app.handlers.view import Login, Schedule, Score, UserInfo

url_patterns = [
    (r'/', Index),
    (r'/rss', Rss),
    (r'/school-list', SchoolList),
    (r'/login', Login),
    (r'/schedule', Schedule),
    (r'/score', Score),
    (r'/user-info', UserInfo),
]
