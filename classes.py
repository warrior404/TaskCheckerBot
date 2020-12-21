#!/usr/bin/python3.7


class User:
    def __init__(self, username):
        self.username = username
        self.timer = 60*60
        self.utc_offset = None
        self.tz_start_time = None
        self.start_time = None
        self.end_time = None
        self.tasks = {}


class Task:
    def __init__(self, message):
        self.message = message
        self.username = None
        self.start_time = None
