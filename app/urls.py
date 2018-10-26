# -*- coding: utf-8 -*-
from app.handlers.view import Login, Schedule

url_patterns = [
    (r'/login/', Login),
    (r'/schedule', Schedule),

]
