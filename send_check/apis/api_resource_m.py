# -*- coding: utf-8 -*-
from configurations import config
from send_check.apis.api_template import ApiTemplate
from urllib.parse import urljoin


def get_create_resource_template_cpu_req(token, cpu, memory):
    # 获取创建CPU模型请求
    path = '/resource-manager/api/v1/resource_templates'
    req = ApiTemplate()
    req.url = urljoin(config.base_url, path)
    req.method = 'post'
    req.headers = {'Authorization': token, "Content-Type": "application/json"}
    req.body = {
        "cpu": cpu,
        "memory": memory,
        "templateType": "CPU",

    }
    return req


def get_delete_resource_template_req(token, uuid):
    # 获取删除CPU模型请求
    path = '/resource-manager/api/v1/resource_templates/{}'.format(uuid)
    req = ApiTemplate()
    req.url = urljoin(config.base_url, path)
    req.method = 'delete'
    req.headers = {'Authorization': token}

    return req


def get_create_resource_template_gpu_req(token, label, count):
    # 获取创建GPU模型请求
    path = '/resource-manager/api/v1/resource_templates'
    req = ApiTemplate()
    req.url = urljoin(config.base_url, path)
    req.method = 'post'
    req.headers = {'Authorization': token, "Content-Type": "application/json"}
    req.body = {
        "label": label,
        "count": count,
        "templateType": "GPU",

    }
    return req


def get_resource_template_info_req(token):
    # 获取资源模板信息请求
    path = '/resource-manager/api/v1/resource_templates'
    req = ApiTemplate()
    req.url = urljoin(config.base_url, path)
    req.method = 'get'
    req.headers = {'Authorization': token}

    return req