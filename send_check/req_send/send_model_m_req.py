# -*- coding: utf-8 -*-

from send_check.apis import api_model_m
from send_check.req_send import send_req


def create_model(token, model_name, labels=['autotest'], description='automation test',
                 model_type='auto',users=None, groups=None, share_type="PRIVATE", is_public=False, resultcode='201'):
    """
    创建新模型
    :param token:
    :param model_name:
    :param description:
    :param labels: list of string
    :return:
    """
    req = api_model_m.get_create_model_req(token=token, model_name=model_name, labels=labels, description=description,
                model_type=model_type,users=users, groups=groups, share_type=share_type, is_public=is_public)
    if resultcode is '201':
        res = send_req.send_request(req, resultcode)
        return res['uuid']
    else:
        send_req.send_request(req, resultcode)
        return True


def modify_model(token, uuid, model_name, labels=['autotest'], description='automation test',
                model_type='auto', share_type="PRIVATE", is_public=False):
    '''
    修改模型
    :param token:
    :param uuid:
    :param model_name:
    :param labels:
    :param description:
    :param model_type:
    :param share_type:
    :param is_public:
    :return:
    '''
    req = api_model_m.get_modify_model_req(token=token, uuid=uuid, model_name=model_name, labels=labels,
                                           description=description, model_type=model_type, share_type=share_type,
                                           is_public=is_public)
    res = send_req.send_request(req)
    return res


def delete_model(token, uuid, resultcode='204'):
    """
    删除模型
    :param token:
    :param uuid:
    :return:
    """
    req = api_model_m.get_delete_model_req(token, uuid)
    send_req.send_request(req, resultcode)


def share_model_and_cancel(token, uuid, share_type, is_public, users=None, groups=None):
    '''
    共享/取消共享模型
    :param token:
    :param uuid:
    :param shareType:
    :param isPublic:
    :param users:
    :param groups:
    :return:
    '''
    req = api_model_m.get_share_model_req(token, uuid, share_type, is_public, users, groups)
    send_req.send_request(req)

def create_model_version(token, model_id, model_path, description='automation test model'):
    """
    创建模型版本
    :param token:
    :param model_id:
    :param model_path:
    :param description:
    :return:
    """
    req = api_model_m.get_create_model_version_req(token, model_id, model_path, description)
    res = send_req.send_request(req, '201')
    return {'uuid': res['uuid'], 'version': res['version_name']}


def modity_model_version(token, model_id, version_id, model_path, description='automation test model'):
    '''
    修改模型版本
    :param token:
    :param model_id:
    :param model_path:
    :param description:
    :return:
    '''
    req = api_model_m.get_modify_model_req(token, model_id, version_id, model_path, description)
    send_req.send_request(req)


def delete_model_version(token, model_uuid, version_uuid, resultcode='204'):
    """
    删除模型版本
    :param token:
    :param model_uuid:
    :param version_uuid:
    :return:
    """
    req = api_model_m.get_delete_model_version_req(token, model_uuid, version_uuid)
    send_req.send_request(req, resultcode)

def create_model_service(token, name, modelId, runtimeImage, cpu, memory,
                         description='auto test description', versionName='v1', instances=1, apiParams=None,
                         apiExamples=None):
    '''
    创建模型服务
    :param token:
    :param name:
    :param modelId:
    :param runtimeImage:
    :param runtimeResource:
    :param description:
    :param versionName:
    :param instances:
    :param apiParams:
    :param apiExamples:
    :return:
    '''
    req = api_model_m.get_create_model_service_req(token, name, modelId, runtimeImage, cpu, memory, description,
                                                   versionName, instances, apiParams, apiExamples)
    res = send_req.send_request(req, '201')
    return res['uuid']


def delete_model_service(token, uuid):
    '''
    删除模型服务
    :param token:
    :param uuid:
    :return:
    '''
    req = api_model_m.get_delete_model_service_req(token, uuid)
    send_req.send_request(req, '204')

def start_model_service(token, uuid):
    '''
    启动模型服务
    :param token:
    :param uuid:
    :return:
    '''
    req = api_model_m.get_start_model_service_req(token, uuid)
    send_req.send_request(req, '201')

def stop_model_service(token, uuid):
    '''
    停止模型服务
    :param token:
    :param uuid:
    :return:
    '''
    req = api_model_m.get_stop_model_service_req(token, uuid)
    send_req.send_request(req, '201')

def get_model_info(token, model_uuid, resultcode='200'):
    '''
    查看模型信息
    :param token:
    :param model_uuid:
    :return:
    '''
    req = api_model_m.get_model_info_req(token, model_uuid)
    res = send_req.send_request(req, resultcode)
    return res


def get_model_version_info(token, model_uuid, version_uuid, resultcode='200'):
    """
    查看模型版本信息
    :param token:
    :param model_uuid:
    :param version_uuid:
    :return:
    """
    req = api_model_m.get_model_version_info_req(token, model_uuid, version_uuid)
    res = send_req.send_request(req, resultcode)
    return res


def get_version_list_by_model(token, model_id, expected_result='200'):
    """
    获取model下的version列表
    :param token:
    :param model_id:
    :param expected_result:
    :return:
    """
    req = api_model_m.get_version_from_model_req(token, model_id)
    res = send_req.send_request(req, expected_result)


def offline_model_version(token, model_id, version_id, expected_result='200'):
    """
    下线/停止模型版本
    :param token:
    :param model_id:
    :param version_id:
    :param expected_result:
    :return:
    """
    req = api_model_m.get_offline_version_req(token, model_id, version_id)
    res = send_req.send_request(req, expected_result)
