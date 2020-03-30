# -*- coding: utf-8 -*-
from urllib.parse import urljoin

from configurations import config
from send_check.apis.api_template import ApiTemplate


def get_create_model_req(token, model_name, model_path='', labels=['autotest'], description='automation test',
                         model_type='auto',users=None, groups=None, share_type="PRIVATE", is_public=False):
    # 获取创建模型请求
    req = ApiTemplate()
    req.path = '/model-manager/api/v1/models'
    req.url = urljoin(config.base_url, req.path)
    req.method = 'post'
    req.headers = {'Authorization': token, "Content-Type": "application/json"}

    req.body = {
        "name": model_name,
        "description": description,
        "labels": labels,
        "modelPath": model_path,
        "modelType": model_type,
        "users": [] if users is None else users,
        "groups": [] if groups is None else groups,
        "shareType": share_type,
        "isPublic": is_public
    }
    return req


def get_modify_model_req(token, uuid, model_name, labels=['autotest'], description='automation test',
                         model_type='auto', share_type="PRIVATE", is_public=False):
    # 获取更新模型请求
    req = ApiTemplate()
    req.path = '/model-manager/api/v1/models/{}'.format(uuid)
    req.url = urljoin(config.base_url, req.path)
    req.method = 'patch'
    req.headers = {'Authorization': token, "Content-Type": "application/json"}
    req.body = {
        "name": model_name,
        "description": description,
        "labels": labels,
        "modelType": model_type,
        "shareType": share_type,
        "isPublic": is_public
    }
    return req


def get_delete_model_req(token, uuid):
    # 获取删除模型请求
    req = ApiTemplate()
    req.path = '/model-manager/api/v1/models/{}'.format(uuid)
    req.url = urljoin(config.base_url, req.path)
    req.method = 'delete'
    req.headers = {'Authorization': token}

    return req


def get_share_model_req(token, uuid, shareType="PRIVATE", isPublic=False, users=None, groups=None):
    # 获取共享模型请求
    req = ApiTemplate()
    req.path = '/model-manager/api/v1/models/{}'.format(uuid)
    req.url = urljoin(config.base_url, req.path)
    req.method = 'patch'
    req.headers = {'Authorization': token, "Content-Type": "application/json"}
    req.body = {
        "shareType": shareType,
        "users": [] if users is None else users,
        "groups": [] if groups is None else groups,
        "isPublic": isPublic
    }
    return req


def get_create_model_version_req(token, model_id, model_path, description):
    # 获取创建模型版本请求
    req = ApiTemplate()
    req.path = '/model-manager/api/v1/models/{}/versions'.format(model_id)
    req.url = urljoin(config.base_url, req.path)
    req.method = 'post'
    req.headers = {'Authorization': token}
    req.body = {
        "modelPath": model_path,
        "description": description
    }
    return req


def get_modify_model_version_req(token, model_id, version_id, model_path, description):
    # 获取修改模型版本请求
    req = ApiTemplate()
    req.path = '/model-manager/api/v1/models/{}/versions/{}'.format(model_id, version_id)
    req.url = urljoin(config.base_url, req.path)
    req.method = 'patch'
    req.headers = {'Authorization': token, "Content-Type": "application/json"}
    req.body = {
        "modelPath": model_path,
        "description": description
    }
    return req


def get_delete_model_version_req(token, model_uuid, version_uuid):
    # 获取删除模型版本请求
    req = ApiTemplate()
    req.path = '/model-manager/api/v1/models/{}/versions/{}'.format(model_uuid, version_uuid)
    req.url = urljoin(config.base_url, req.path)
    req.method = 'delete'
    req.headers = {'Authorization': token}

    return req


def get_create_model_service_req(token, name, modelId, runtimeImage, cpu, memory,
                                 description='auto test description', versionName='v1', instances=1, apiParams=None,
                                 apiExamples=None):
    # 获取创建模型服务请求
    req = ApiTemplate()
    req.path = '/model-manager/api/v1/services'
    req.url = urljoin(config.base_url, req.path)
    req.method = 'post'
    req.headers = {'Authorization': token, "Content-Type": "application/json"}
    req.body = {
        "name": name,
        "description": description,
        "modelId": modelId,
        "versionName": versionName,
        "runtimeImage": runtimeImage,
        "instances": instances,
        "runtimeResource": {
            "cpus": cpu,
            "memory": memory
        },
        "apiParams": {"input": [], "output": []} if apiParams is None else apiParams,
        "apiExamples": {"requests": [],
                        "response": {"success": '', "failed": ''}} if apiExamples is None else apiExamples
    }

    return req


def get_delete_model_service_req(token, uuid):
    # 获取删除模型服务请求
    req = ApiTemplate()
    req.path = '/model-manager/api/v1/services{}'.format(uuid)
    req.url = urljoin(config.base_url, req.path)
    req.method = 'delete'
    req.headers = {'Authorization': token}

    return req

def get_start_model_service_req(token, uuid):
    # 获取启动模型服务请求
    req = ApiTemplate()
    req.path = '/model-manager/api/v1/services/{}/start'.format(uuid)
    req.url = urljoin(config.base_url, req.path)
    req.method = 'post'
    req.headers = {'Authorization': token, "Content-Type": "application/json"}

    return req

def get_stop_model_service_req(token, uuid):
    # 获取停止模型服务请求
    req = ApiTemplate()
    req.path = '/model-manager/api/v1/services/{}/stop'.format(uuid)
    req.url = urljoin(config.base_url, req.path)
    req.method = 'post'
    req.headers = {'Authorization': token, "Content-Type": "application/json"}

    return req

def get_model_info_req(token, model_uuid):
    # 获取查看模型请求
    req = ApiTemplate()
    req.path = '/model-manager/api/v1/models/{}'.format(model_uuid)
    req.url = urljoin(config.base_url, req.path)
    req.method = 'get'
    req.headers = {'Authorization': token}

    return req


def get_model_version_info_req(token, model_uuid, version_uuid):
    # 获取查看模型版本请求
    req = ApiTemplate()
    req.path = '/model-manager/api/v1/models/{}/versions/{}'.format(model_uuid, version_uuid)
    req.url = urljoin(config.base_url, req.path)
    req.method = 'get'
    req.headers = {'Authorization': token}

    return req


def get_version_from_model_req(token, model_id):
    # 获取通过modelId查询version的请求
    req = ApiTemplate()
    req.path = '/model-manager/api/v1/models/{}/versions'.format(model_id)
    req.url = urljoin(config.base_url, req.path)
    req.method = 'get'
    req.headers = {'Authorization': token}

    return req


def get_offline_version_req(token, model_id, version_uuid):
    # 获取下线模型版本请求
    req = ApiTemplate()
    req.path = '/model-manager/api/v1/models/{}/versions/{}/stop'.format(model_id, version_uuid)
    req.url = urljoin(config.base_url, req.path)
    req.method = 'post'
    req.headers = {'Authorization': token}

    return req
