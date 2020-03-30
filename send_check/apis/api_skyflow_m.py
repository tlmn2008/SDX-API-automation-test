# -*- coding: utf-8 -*-
from configurations import config
from send_check.apis.api_template import ApiTemplate
from urllib.parse import urljoin


def get_create_skyflow_req(token, name, process_type, description, is_template=False, users=[], groups=[],
                           skyflow_template=""):
    # 获取创建skyflow请求
    path = '/skyflow-manager/api/v1/skyflows'
    req = ApiTemplate()
    req.url = urljoin(config.base_url, path)
    req.method = 'post'
    req.headers = {'Authorization': token, "Content-Type": "application/json"}
    req.body = {
        "name": name,
        "description": description,
        "processType": process_type,
        "isTemplate": is_template,
        "users": users,
        "groups": groups,
        "skyflowTemplate": skyflow_template

    }
    return req


def get_delete_skyfow_req(token, uuid):
    # 获取删除skyflow请求
    path = '/skyflow-manager/api/v1/skyflows/{}'.format(uuid)
    req = ApiTemplate()
    req.url = urljoin(config.base_url, path)
    req.method = 'delete'
    req.headers = {'Authorization': token}

    return req

"""
description: "describ"
groups: []
isTemplate: false
name: "testflow"
processType: "PATCH"
skyflowTemplate: ""
users: []
"""

"""
description: ""
groups: []
isTemplate: true
name: "test"
processType: "PATCH"
skyflowTemplate: "轨道交通"
users: []
"""
