# -*- coding: utf-8 -*-
from send_check.apis import api_resource_m
from send_check.req_send import send_req


def create_resource_template_cpu(token, cpu, memory):
    """

    :param token:
    :param cpu:
    :param memory:
    :return:
    """
    req = api_resource_m.get_create_resource_template_cpu_req(token=token, cpu=cpu, memory=memory)
    res = send_req.send_request(req, '202')
    return res['uuid']


def create_resource_template_gpu(token, label='gtx-1080', count=16):
    """

    :param token:
    :param label:
    :param count:
    :return:
    """
    req = api_resource_m.get_create_resource_template_gpu_req(token=token, label=label, count=count)
    res = send_req.send_request(req, '202')
    return res['uuid']


def delete_resource_template(token, uuid):
    """

    :param token:
    :param uuid:
    :return:
    """
    req = api_resource_m.get_delete_resource_template_req(token, uuid)
    res = send_req.send_request(req, '204')
    return res


def get_select_resource_template_info(token, select):
    '''
    选择资源模板后返回模板中的cpu和memory信息，供任务或服务使用，select值从0开始
    :param token:
    :param select:
    :return:
    '''
    req = api_resource_m.get_resource_template_info_req(token)
    res = send_req.send_request(req)
    resource = {
        "cpu": res['items'][select]['cpu'],
        "memory": res['items'][select]['memory']
    }
    return resource