# -*- coding: utf-8 -*-
from locust import HttpLocust, TaskSet, between


def send_req(l):
    method = 'get'
    paths = '/get1/headers'
    l.client.request(method=method, url=paths)


class UserBehavior(TaskSet):
    tasks = {
            send_req
             }

    def on_start(self):

        pass

    def on_stop(self):
        pass


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    wait_time = between(1, 1)

