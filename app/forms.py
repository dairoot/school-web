# -*- coding: utf-8 -*-
from schema import Schema

time_channles_schema = Schema({
    'time_start': int,
    'time_stop': int,
    'channels': [str]
})

channels_schema = Schema({
    'channels': [str]
})

particle_time_channles_schema = Schema({
    'time_start': int,
    'channels': [str],
    'particle': int,
})

times_channels_schema = Schema({
    'times': [int],
    'channels': [str]
})

role_ids_schema = Schema({
    'role_ids': str
})
