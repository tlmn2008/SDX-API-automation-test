# -*- coding: utf-8 -*-

from send_check.apis import api_storage_m
from send_check.req_send import send_req


def get_user_ceph_path(token):
    '''
    获取用户文件存储的ceph路径
    :param token:
    :param description:
    :return:
    '''
    req = api_storage_m.get_user_volume_id_req(token=token)
    res = send_req.send_request(req)
    path = res["volumes"][0]["path"]
    return path
