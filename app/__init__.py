# -*- coding: utf-8 -*-
from redis import Redis

redis = Redis(decode_responses=True)
redis_school = Redis()
