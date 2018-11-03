# -*- coding: utf-8 -*-
from app.handlers.view import Login, Schedule, Score, UserInfo

url_patterns = [
    (r'/login/', Login),
    (r'/schedule', Schedule),
    (r'/score', Score),
    (r'/user-info', UserInfo),
]
