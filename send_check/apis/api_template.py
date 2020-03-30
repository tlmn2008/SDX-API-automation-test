# -*- coding: utf-8 -*-


class ApiTemplate(object):

    def __init__(self):
        self.method = ''
        self.path = ''
        # url={SDX IP:port}/{path}
        self.url = ''
        self.param = {}
        self.headers = {}
        self.body = {}
        self.files = {}
