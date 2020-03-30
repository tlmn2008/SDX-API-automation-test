# -*- coding: utf-8 -*-

import json
import datetime

from locust import HttpLocust, TaskSet, between
from send_check.apis.api_compose import *
from send_check.apis import api_file_m
from send_check.apis import api_model_m
from send_check.req_send import send_req


token = None
file_share_id = None
current_models = []
model_version = {}
user_id = 'e7505442-6a47-45d8-8179-05913f7cd4f4'  # user1: tengliang
share_user1 = "f73cdd19-fe63-4d85-b864-47da8a210659"  # user2
share_user2 = "4774ddb8-7459-4ad5-9f7b-2278b6bd181f"  # user3
share_file_path = '/tengliang/t.jpg'


def joint_param_into_url(url, param):
    # 拼接HTTP请求
    url = url + '?' if len(param) > 0 else url
    for i, j in param.items():
        if url.endswith('?'):
            url = '{}{}={}'.format(url, i, j)
        else:
            url = '{}&{}={}'.format(url, i, j)
    return url


def compose_user_login(l=None):
    global token
    req = get_compose_user_login_req()
    if l is not None:
        resp = l.client.request(method=req.method, headers=req.headers, url=req.path, json=req.body)
        try:
            result = json.loads(str(resp.content, 'utf-8'))
            token = f"Bearer {result['accessToken']}"
        except Exception:
            print("can not get token!")
            print('resp is {}'.format(resp.content))
            return False
    else:
        # on_start执行时调用
        resp = send_req.send_request(req)

        try:
            token = f"Bearer {resp['accessToken']}"
        except Exception:
            print("can not get token!")
            print('resp is {}'.format(resp.content))
            return False


def compose_user_detail(l):

    uuid = user_id
    req = get_compose_user_detail_req(token, uuid)
    l.client.request(method=req.method, headers=req.headers, url=req.path, json=req.body)


def compose_user_list(l):

    req = get_compose_user_list_req(token, roles='1c351df4-a9b7-4895-8111-b1fbc42d704b')
    req.path = joint_param_into_url(req.path, req.param)
    l.client.request(method=req.method, headers=req.headers, url=req.path, json=req.body)


def compose_user_group_list(l):

    req = get_compose_user_group_list_req(token, uuids='bb45efd6-c6c4-4543-a502-2875cc1d3746')
    req.path = joint_param_into_url(req.path, req.param)
    l.client.request(method=req.method, headers=req.headers, url=req.path, json=req.body)


def compose_file_list(l):
    # 获取文件列表
    req = get_compose_file_list_req(token, owner_id=user_id, file_path='/')
    req.path = joint_param_into_url(req.path, req.param)
    l.client.request(method=req.method, headers=req.headers, url=req.path, json=req.body)


def compose_shared_file_list(l):
    # 获取共享文件列表
    req = get_compose_shared_file_list_req(token, owner_id=user_id, file_path=share_file_path)  # user_id=share_user1
    req.path = joint_param_into_url(req.path, req.param)
    resp = l.client.request(method=req.method, headers=req.headers, url=req.path, json=req.body)
    # 取得文件share id，供取消共享接口使用
    global file_share_id
    result = None
    if resp.content:
        result = json.loads(str(resp.content, 'utf-8'))

    if 'children' in result:
        for i in result['children']:
            if i['path'] == share_file_path:
                file_share_id = i['fileShareId']


def cancel_shared_file(l):
    # 取消文件共享
    if file_share_id:
        req = api_file_m.get_cancel_shared_file_req(token, file_share_id)
        req.path = joint_param_into_url(req.path, req.param)
        l.client.request(method=req.method, headers=req.headers, url=req.path, json=req.body)


def compose_file_share_batch(l):
    # 文件批量共享
    req = get_compose_file_share_batch_req(token, paths=[share_file_path], owner_id=user_id, share_id=user_id)
    l.client.request(method=req.method, headers=req.headers, url=req.path, json=req.body)


def cancel_and_share_file_batch(l):
    compose_shared_file_list(l)
    cancel_shared_file(l)
    compose_file_share_batch(l)


def compose_image_list(l):
    # 获取镜像列表
    req = get_compose_image_list_req(token, name='iluvatar', build_type='BASIC', image_type='TENSORFLOW_DEPLOYMENT')
    req.path = joint_param_into_url(req.path, req.param)
    l.client.request(method=req.method, headers=req.headers, url=req.path, json=req.body)


def compose_image_builder_list(l):
    # 获取镜像构建列表
    req = get_compose_image_builder_list_req(token, state='FINISHED', build_type='ONLINE', image_type='JUPYTER')
    req.path = joint_param_into_url(req.path, req.param)
    l.client.request(method=req.method, headers=req.headers, url=req.path, json=req.body)


def compose_image_share_batch(l):
    # 镜像批量共享
    share_image_uuid = '746e6275-7c85-4a50-9b29-0ac3a23e0bf9'
    req = get_compose_image_share_batch_req(token, uuids=[share_image_uuid], shareType='PUBLIC',
                                            users=[share_user1, share_user2])
    l.client.request(method=req.method, headers=req.headers, url=req.path, json=req.body)


def compose_image_delete_batch(l):
    # 镜像批量共享
    req = get_compose_image_delete_batch_req(token, uuids=["abcd-abcd-abcd-abcd", "cccc-cccc-cccc-cccc"])
    l.client.request(method=req.method, headers=req.headers, url=req.path, json=req.body)


def compose_model_list(l):
    # 获取模型列表
    req = get_compose_model_list_req(token, name='ptest')  # 查询性能测试model
    req.path = joint_param_into_url(req.path, req.param)
    resp = l.client.request(method=req.method, headers=req.headers, url=req.path, json=req.body)

    # 提取当前性能测试model的uuid, 供version停止、model删除接口使用
    global current_models
    if resp.content:
        result = json.loads(str(resp.content, 'utf-8'))
        tmp_model_list = []
        for model in result['items']:
            tmp_model_list.append(model['uuid'])
        current_models = tmp_model_list


def fetch_version_from_model(l):
    version_list = {}
    for model in current_models:
        req = api_model_m.get_version_from_model_req(token, model)
        resp = l.client.request(method=req.method, headers=req.headers, url=req.path)

        if str(resp.status_code).startswith('2'):
            result = json.loads(str(resp.content, 'utf-8'))
            tmp_model_version = {}
            # 待改进，只记录了model的最后一个version uuid
            for version in result['items']:
                tmp_model_version[model] = version['uuid']
            version_list.update(tmp_model_version)
    global model_version
    model_version = version_list


def stop_version(l):
    model_ids = model_version.keys()
    for model_id in model_ids:
        req = api_model_m.get_offline_version_req(token, model_id, model_version[model_id])
        l.client.request(method=req.method, headers=req.headers, url=req.path, json=req.body)


def fetch_model_and_stop_version(l):
    compose_model_list(l)
    fetch_version_from_model(l)
    stop_version(l)


def compose_model_share_batch(l):
    # 模型批量共享
    share_model_uuid = 'a548687e-01ed-456a-9679-01a6ad341207'
    req = get_compose_model_share_batch_req(token, uuids=[share_model_uuid], shareType='PUBLIC',
                                            users=[share_user1, share_user2])
    l.client.request(method=req.method, headers=req.headers, url=req.path, json=req.body)


def compose_model_deploy(l):
    # 模型部署
    timestamp = datetime.datetime.now().strftime('%d_%H.%M.%S.%f')
    model_name = 'ptest_model_{}'.format(timestamp)
    version_name = 'ptest_ver_{}'.format(timestamp)

    runtime_resource = {"cpuObj": {"cpu": 1, "memory": 2, "uuid": "1-2"}, "gpuObj": {}, "cpu": 1000, "memory":2147483648}

    req = get_compose_model_deploy_req(token, model_name=model_name, version_name=version_name,
                                       framework='TENSORFLOW', runtime_image='tensorflow_deployment:latest',
                                       runtime_resource=runtime_resource, model_path='/')
    resp = l.client.request(method=req.method, headers=req.headers, url=req.path, json=req.body)


def compose_model_delete_batch(l):
    # 模型批量删除
    # Continue, 查询出模型并全部删除
    req = get_compose_model_delete_batch_req(token, uuids=current_models)
    l.client.request(method=req.method, headers=req.headers, url=req.path, json=req.body)


def compose_project_list(l):
    # 模型列表
    req = get_compose_project_list_req(token, project_type='public')
    req.path = joint_param_into_url(req.path, req.param)
    l.client.request(method=req.method, headers=req.headers, url=req.path, json=req.body)


def compose_resource_config_list(l):
    # 获取资源配置列表
    req = get_compose_resource_config_list_req(token)
    l.client.request(method=req.method, headers=req.headers, url=req.path, json=req.body)


def compose_skyflow_list(l):
    # 获取skyflow列表
    req = get_compose_skyflow_list_req(token, name='streamflow', process_type='PATCH')
    req.path = joint_param_into_url(req.path, req.param)
    l.client.request(method=req.method, headers=req.headers, url=req.path, json=req.body)


def compose_task_list(l):
    # 任务列表
    req = get_compose_task_list_req(token, username='teng', name='streamflow')
    req.path = joint_param_into_url(req.path, req.param)
    l.client.request(method=req.method, headers=req.headers, url=req.path, json=req.body)


def compose_task_detail(l):
    # 任务详情
    task_uuid = 'bc3d1e54-cbcb-42bd-965c-a6316320b5c4' # 'bb454151-e4fb-41aa-a44c-276b8ad7f851'
    req = get_compose_task_detail_req(token, uuid=task_uuid)
    req.path = joint_param_into_url(req.path, req.param)
    l.client.request(method=req.method, headers=req.headers, url=req.path, json=req.body)


def compose_task_execution_list(l):
    # 执行任务列表
    req = get_compose_task_execution_list_req(token)
    req.path = joint_param_into_url(req.path, req.param)
    l.client.request(method=req.method, headers=req.headers, url=req.path, json=req.body)


def compose_task_resource(l):
    # 执行任务占用资源
    req = get_compose_task_resource_req(token)
    req.path = joint_param_into_url(req.path, req.param)
    l.client.request(method=req.method, headers=req.headers, url=req.path, json=req.body)


class UserBehavior(TaskSet):
    tasks = {
             compose_user_login,
             compose_user_detail,
             compose_user_list,
             compose_user_group_list,
             compose_file_list,
             cancel_and_share_file_batch,
             # compose_shared_file_list,
             compose_image_list,
             compose_image_builder_list,
             # compose_image_share_batch,
             # compose_image_delete_batch,
             fetch_model_and_stop_version,
             compose_model_list,
             # compose_model_share_batch,
             # compose_model_deploy,
             compose_model_delete_batch,
             compose_project_list,
             compose_resource_config_list,
             compose_skyflow_list,
             compose_task_list,
             # compose_task_detail
             compose_task_execution_list,
             compose_task_resource
            }

    def on_start(self):
        compose_user_login()
        pass

    def on_stop(self):
        pass


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    wait_time = between(1, 1)




