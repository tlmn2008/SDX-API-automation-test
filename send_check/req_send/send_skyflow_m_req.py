# -*- coding: utf-8 -*-

from send_check.apis import api_skyflow_m
from send_check.apis import api_compose
from send_check.req_send import send_req


def create_skyflow_batch(token, name, description="automation test skyflow batch", is_template=False, users=[],
                         groups=[], skyflow_template=""):

    req = api_skyflow_m.get_create_skyflow_req(token, name, process_type='batch', description=description, is_template=is_template,
                                               users=users, groups=groups, skyflow_template=skyflow_template)
    res = send_req.send_request(req, '200')
    return res['uuid']


def create_skyflow_stream(token, name, description="automation test skyflow stream", is_template=False, users=[],
                          groups=[], skyflow_template=""):

    req = api_skyflow_m.get_create_skyflow_req(token, name, process_type='stream', description=description,
                                               is_template=is_template, users=users, groups=groups,
                                               skyflow_template=skyflow_template)
    res = send_req.send_request(req, '200')
    return res['uuid']


def delete_skyflow(token, uuid):
    req = api_skyflow_m.get_delete_skyfow_req(token, uuid)
    res = send_req.send_request(req, '200')


def get_skyflow_list(token, name=None, process_type=None, start=1,
                     count=1000, order='desc', order_by='createdAt'):
    """
    获取skyflow列表
    Args:
        token: 用户token
        name: skyflow项目名称
        process_type: process类型, 例如public
        start: 起始编号
        count: 截至编号
        order: 排序方式, 升序或降序
        order_by: 排序依据

    Returns:
        skyflow_list: skyflow列表, 包含模板类型在内.

    """
    req = api_compose.get_compose_skyflow_list_req(
        token, name=name, process_type=process_type, start=start,
        count=count, order=order, order_by=order_by)

    skyflow_list = send_req.send_request(req)

    req = api_compose.get_compose_skyflow_list_req(
        token, name=name, process_type=process_type, start=start,
        count=count, order=order, order_by=order_by, is_template=True)

    skyflow_list += send_req.send_request(req)

    return skyflow_list
