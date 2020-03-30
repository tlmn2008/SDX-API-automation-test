# -*- coding: utf-8 -*-
from configurations import config
from send_check.apis.api_template import ApiTemplate
from urllib.parse import urljoin


def get_create_new_project_req(token, project_name='auto test project', description='automation test', is_template=False, users=None, groups=None, model_id=''):
    path = '/project-manager/api/v1/projects/'
    req = ApiTemplate()
    req.url = urljoin(config.base_url, path)
    req.method = 'post'
    req.headers = {'Authorization': token, "Content-Type": "application/json"}
    if model_id == '':
        req.body = {
            "name": project_name,
            "description": description,
            "isTemplate": is_template,
            "users": [] if users is None else users,
            "groups": [] if groups is None else groups
            }
    else:
        req.body = {
            "uuid": model_id
        }
    return req


def get_delete_project_req(token, uuid):
    path = '/project-manager/api/v1/projects/{}'.format(uuid)
    req = ApiTemplate()
    req.url = urljoin(config.base_url, path)
    req.method = 'delete'
    req.headers = {'Authorization': token}
    return req


def get_entry_project_req(token, uuid):
    path = '/project-manager/api/v1/projects/{}'.format(uuid)
    req = ApiTemplate()
    req.url = urljoin(config.base_url, path)
    req.method = 'get'
    req.headers = {'Authorization': token}
    return req


def get_create_task_req(token, task_name, project_id, task_type, image_id, resource_config=None,
                        description='automation test task'):
    if resource_config is None:
        resource_config = {"EXECUTOR_CPUS": 4000, "EXECUTOR_GPUS": 0, "EXECUTOR_INSTANCES": 1,
                           "EXECUTOR_MEMORY": 8589934592, "GPU_MODEL": ""}

    path = '/project-manager/api/v1/tasks'
    req = ApiTemplate()
    req.url = urljoin(config.base_url, path)
    req.method = 'post'
    req.headers = {'Authorization': token, "Content-Type": "application/json"}
    req.body = {
        "projectId": project_id,
        "name": task_name,
        "description": description,
        "type": task_type,
        "imageId": image_id,
        "resourceConfig": resource_config
    }
    return req


def get_start_task_req(token, task_id, is_auto=False):
    path = '/project-manager/api/v1/tasks/{}/start'.format(task_id)
    req = ApiTemplate()
    req.url = urljoin(config.base_url, path)
    req.method = 'post'
    req.headers = {'Authorization': token, "Content-Type": "application/json"}
    req.body = {
        "isAuto": is_auto
    }
    return req


def get_task_info_req(token, task_id):
    path = '/project-manager/api/v1/tasks/{}'.format(task_id)
    req = ApiTemplate()
    req.url = urljoin(config.base_url, path)
    req.method = 'get'
    req.headers = {'Authorization': token}
    return req


def get_stop_task_req(token, task_id, need_commit_container=False, auto_image_name='', auto_image_version=''):
    path = '/project-manager/api/v1/tasks/{}/stop'.format(task_id)
    req = ApiTemplate()
    req.url = urljoin(config.base_url, path)
    req.method = 'post'
    req.headers = {'Authorization': token, "Content-Type": "application/json"}
    req.body = {
        "needCommitContainer": need_commit_container,
        "autoImageName": auto_image_name,
        "autoImageVersion": auto_image_version
    }
    return req


def get_delete_task_req(token, task_id):
    path = '/project-manager/api/v1/tasks/{}'.format(task_id)
    req = ApiTemplate()
    req.url = urljoin(config.base_url, path)
    req.method = 'delete'
    req.headers = {'Authorization': token}
    return req
