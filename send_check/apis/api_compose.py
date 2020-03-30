# -*- coding: utf-8 -*-


from configurations import config
from send_check.apis.api_template import ApiTemplate
from urllib.parse import urljoin
from utilities.common_method import remove_None_value_elements


def get_compose_user_login_req(username=config.user_name_a, password=config.user_passwd_a):
    # 获取聚合-用户登录请求
    req = ApiTemplate()
    req.path = '/gateway/fe-compose/api/v1/login'
    req.url = urljoin(config.base_url, req.path)
    req.method = 'post'
    req.body = {
           "grantType": "password",
           "username": username,
           "password": password
        }

    return req


def get_compose_user_detail_req(token, user_uuid):
    # 获取聚合-用户详情请求
    req = ApiTemplate()
    req.path = '/gateway/fe-compose/api/v1/user-detail?uuid={}'.format(user_uuid)
    req.url = urljoin(config.base_url, req.path)
    req.method = 'get'
    req.headers = {'Authorization': token}

    return req


def get_compose_user_list_req(token, username=None, full_name=None, uuids=None, groups=None, roles=None,
                              permissions=None, is_active=True, start=1, count=20, order_by=None, order='asc'):
    # 获取聚合-用户列表请求
    req = ApiTemplate()
    req.path = '/fe-compose/api/v1/user-profiles'
    req.url = urljoin(config.base_url, req.path)
    req.method = 'get'
    req.headers = {'Authorization': token}
    req.param.update({
        "username": username,
        "fullName": full_name,
        "uuids": uuids,
        "groups": groups,
        "roles": roles,
        "permissions": permissions,
        "isActive": is_active,
        "start": start,
        "count": count,
        "orderBy": order_by,
        "order": order,
        }
    )
    # 如果值为None则不传此参数
    req.param = remove_None_value_elements(req.param)
    return req


def get_compose_user_group_list_req(token, username=None, user_ids=None, uuids=None, roles=None, permissions=None,
                                    is_active=True, start=1, count=20, order_by=None, order='asc'):
    # 获取聚合-用户组列表请求
    req = ApiTemplate()
    req.path = '/gateway/fe-compose/api/v1/group-profiles'
    req.url = urljoin(config.base_url, req.path)
    req.method = 'get'
    req.headers = {'Authorization': token}
    req.param.update({
        "username": username,
        "userIds": user_ids,
        "uuids": uuids,
        "roles": roles,
        "permissions": permissions,
        "isActive": is_active,
        "start": start,
        "count": count,
        "orderBy": order_by,
        "order": order,
        }
    )
    # 如果值为None则不传此参数
    req.param = remove_None_value_elements(req.param)
    return req


def get_compose_file_list_req(token, owner_id, file_path, start=1, count=-1, order_by='name', order='asc', show_hidden=0,
                              filesystem='cephfs', file_extension='', only_directory=0, only_file=0, real_path=0):
    # 获取聚合-文件列表请求
    req = ApiTemplate()
    req.path = '/fe-compose/api/v1/file-profiles'
    req.url = urljoin(config.base_url, req.path)
    req.method = 'get'
    req.headers = {'Authorization': token, "Content-Type": "application/json"}
    req.param.update({
        "ownerId": owner_id,
        "path": file_path,
        "start": start,
        "count": count,
        "orderBy": order_by,
        "order": order,
        "showHidden": show_hidden,
        "filesystem": filesystem,
        "fileExtension": file_extension,
        "onlyDirectory": only_directory,
        "onlyFile": only_file,
        "realpath": real_path
        }
    )

    return req


def get_compose_file_share_batch_req(token, paths, owner_id, share_id='', is_global=False, users=None, groups=None):
    # 获取聚合-文件批量分享请求
    req = ApiTemplate()
    req.path = '/fe-compose/api/v1/file-share-batch'
    req.url = urljoin(config.base_url, req.path)
    req.method = 'post'
    req.headers = {'Authorization': token}
    req.body = {
        "paths": paths,
        "ownerId": owner_id,
        "sharerId": share_id,
        "isGlobal": is_global,
        "users": users if users else [],
        "groups": groups if groups else []
    }

    return req


def get_compose_shared_file_list_req(token, owner_id=None, sharerId=None, file_path=None, start=1, count=15,
                                     user_id=None, group_id=None):
    # 获取聚合-共享文件列表请求
    req = ApiTemplate()
    req.path = '/fe-compose/api/v1/file-share-profiles'
    req.url = urljoin(config.base_url, req.path)
    req.method = 'get'
    req.headers = {'Authorization': token}
    req.param.update({
        "ownerId": owner_id,
        "sharerId": sharerId,
        "userId": user_id,
        "groupId": group_id,
        "path": file_path,
        "start": start,
        "count": count,
        }
    )
    # 如果值为None则不传此参数
    req.param = remove_None_value_elements(req.param)
    return req


def get_compose_image_list_req(token, name=None, version=None, project_name=None, image_type=None, share_type=None,
                               build_type=None, owner_id=None, exclude_owner_id=None, start=None, count=None,
                               order=None, order_by=None):
    # 获取聚合-镜像列表请求
    req = ApiTemplate()
    req.path = '/fe-compose/api/v1/image-profiles'
    req.url = urljoin(config.base_url, req.path)
    req.method = 'get'
    req.headers = {'Authorization': token}
    req.param.update({
        "name": name,
        "version": version,
        "projectName": project_name,
        "imageType": image_type,
        "shareType": share_type,
        "buildType": build_type,
        "ownerId": owner_id,
        "excludeOwnerId": exclude_owner_id,
        "start": start,
        "count": count,
        "order": order,
        "orderBy": order_by
        }
    )
    # 如果值为None则不传此参数
    req.param = remove_None_value_elements(req.param)
    return req


def get_compose_image_builder_list_req(token, image_type=None, name=None, version=None, project_name=None, state=None,
                                       build_type=None, start=None, count=None, order=None, order_by=None):
    # 获取聚合-镜像构建列表请求
    req = ApiTemplate()
    req.path = '/gateway/fe-compose/api/v1/image-builder-profiles'
    req.url = urljoin(config.base_url, req.path)
    req.method = 'get'
    req.headers = {'Authorization': token}
    req.param.update({
        "imageType": image_type,
        "name": name,
        "version": version,
        "projectName": project_name,
        "state": state,
        "buildType": build_type,
        "start": start,
        "count": count,
        "order": order,
        "orderBy": order_by
        }
    )
    # 如果值为None则不传此参数
    req.param = remove_None_value_elements(req.param)
    return req


def get_compose_image_share_batch_req(token, uuids, shareType, users=[], groups=[]):
    # 获取聚合-镜像批量共享请求
    req = ApiTemplate()
    req.path = '/gateway/fe-compose/api/v1/image-share-batch'
    req.url = urljoin(config.base_url, req.path)
    req.method = 'post'
    req.headers = {'Authorization': token}
    req.body = {
        "uuids": uuids,
        "setting": {
            "shareType": shareType,
            "users": users,
            "groups": groups
            }
        }

    return req


def get_compose_image_delete_batch_req(token, uuids):
    # 获取聚合-镜像批量删除请求
    req = ApiTemplate()
    req.path = '/gateway/fe-compose/api/v1/image-delete-batch'
    req.url = urljoin(config.base_url, req.path)
    req.method = 'post'
    req.headers = {'Authorization': token}
    req.body = {
        "uuids": uuids
    }

    return req


def get_compose_model_list_req(token, name=None, share_type='ALL', is_public=False, start=1, count=15, order='asc',
                               order_by='createdAt'):
    # 获取聚合-模型列表请求
    req = ApiTemplate()
    req.path = '/gateway/fe-compose/api/v1/model-profiles'
    req.url = urljoin(config.base_url, req.path)
    req.method = 'get'
    req.headers = {'Authorization': token}
    req.param.update({
        "name": name,
        "shareType": share_type,
        "isPublic": is_public,
        "start": start,
        "count": count,
        "order": order,
        "orderBy": order_by
        }
    )
    # 如果值为None则不传此参数
    req.param = remove_None_value_elements(req.param)
    return req


def get_compose_model_share_batch_req(token, uuids, shareType, users=[], groups=[]):
    # 获取聚合-模型批量共享请求
    req = ApiTemplate()
    req.path = '/gateway/fe-compose/api/v1/model-share-batch'
    req.url = urljoin(config.base_url, req.path)
    req.method = 'post'
    req.headers = {'Authorization': token}
    req.body = {
        "uuids": uuids,
        "setting": {
            "shareType": shareType,
            "users": users,
            "groups": groups
            }
        }

    return req


def get_compose_model_deploy_req(token, version_name, model_name=None, model_id=None, description='auto test',
                                 framework=None, runtime_image=None, model_path=None, runtime_resource=None):
    # 获取聚合-模型部署请求
    req = ApiTemplate()
    req.path = '/gateway/fe-compose/api/v1/model-deploy'
    req.url = urljoin(config.base_url, req.path)
    req.method = 'post'
    req.headers = {'Authorization': token}
    req.body = {
        # modelName和modelId两者传一
        "modelName": model_name,
        "modelId": model_id,
        "versionName": version_name,
        "description": description,
        "framework": framework,
        "runtimeImage": runtime_image,
        "modelPath": model_path,
        "runtimeResource": runtime_resource
        }
    req.body = remove_None_value_elements(req.body)

    return req


def get_compose_model_delete_batch_req(token, uuids):
    # 获取聚合-模型批量删除请求
    req = ApiTemplate()
    req.path = '/gateway/fe-compose/api/v1/model-delete-batch'
    req.url = urljoin(config.base_url, req.path)
    req.method = 'post'
    req.headers = {'Authorization': token}
    req.body = {
         "uuids": uuids
        }

    return req


def get_compose_project_list_req(token, name=None, project_type=None, start=1, count=15, order='asc',
                                 order_by='createdAt'):
    # 获取聚合-模型列表请求
    req = ApiTemplate()
    #req.path = '/gateway/fe-compose/api/v1/project-profiles'
    req.path = '/fe-compose/api/v1/project-profiles'
    req.url = urljoin(config.base_url, req.path)
    req.method = 'get'
    req.headers = {'Authorization': token}
    req.param.update({
        "name": name,
        "type": project_type,
        "start": start,
        "count": count,
        "order": order,
        "orderBy": order_by
        }
    )
    # 如果值为None则不传此参数
    req.param = remove_None_value_elements(req.param)
    return req


def get_compose_project_task_list_req(token, uuid):
    # 获取聚合-项目任务列表
    req = ApiTemplate()
    req.path = '/gateway/fe-compose/api/v1/project-task-profiles'
    req.url = urljoin(config.base_url, req.path)
    req.method = 'get'
    req.headers = {'Authorization': token}
    req.param.update({
        "projectId": uuid
        }
    )

    return req


def get_compose_resource_config_list_req(token):
    # 获取聚合-资源配置列表请求
    req = ApiTemplate()
    req.path = '/gateway/fe-compose/api/v1/resource-config-profiles'
    req.url = urljoin(config.base_url, req.path)
    req.method = 'get'
    req.headers = {'Authorization': token}

    return req


def get_compose_skyflow_list_req(token, name, start=1, count=15, order='desc',
                                 order_by='createdAt', process_type=None, is_template=False):
    # 获取聚合-skyflow列表请求
    req = ApiTemplate()
    # req.path = '/gateway/fe-compose/api/v1/skyflow-profiles'
    req.path = '/fe-compose/api/v1/skyflow-profiles'
    req.url = urljoin(config.base_url, req.path)
    req.method = 'get'
    req.headers = {'Authorization': token}
    req.param.update({
        "name": name,
        "start": start,
        "count": count,
        "order": order,
        "orderBy": order_by,
        "processType": process_type,
        "isTemplate": is_template
        }
    )
    # 如果值为None则不传此参数
    req.param = remove_None_value_elements(req.param)
    return req


def get_compose_task_list_req(token, username, name, is_active=True, start=1, count=15, order='desc',
                              order_by='createdAt'):
    # 获取聚合-任务列表请求
    req = ApiTemplate()
    req.path = '/gateway/fe-compose/api/v1/task-profiles'
    req.url = urljoin(config.base_url, req.path)
    req.method = 'get'
    req.headers = {'Authorization': token}
    req.param.update({
        "username": username,
        "name": name,
        "isActive": is_active,
        "start": start,
        "count": count,
        "order": order,
        "orderBy": order_by
        }
    )
    # 如果值为None则不传此参数
    req.param = remove_None_value_elements(req.param)
    return req


def get_compose_task_detail_req(token, uuid):
    # 获取聚合-任务详情请求
    req = ApiTemplate()
    req.path = '/gateway/fe-compose/api/v1/task-detail'
    req.url = urljoin(config.base_url, req.path)
    req.method = 'get'
    req.headers = {'Authorization': token}
    req.param.update({
        "uuid": uuid
        }
    )
    return req


def get_compose_task_execution_list_req(token, start=1, count=10,
                                        order='desc', order_by='startedAt'):
    # 获取聚合-任务执行列表请求
    req = ApiTemplate()
    req.path = '/gateway/fe-compose/api/v1/task-execution-profiles'
    req.url = urljoin(config.base_url, req.path)
    req.method = 'get'
    req.headers = {'Authorization': token}
    req.param.update({
        "start": start,
        "count": count,
        "order": order,
        "orderBy": order_by
        }
    )
    return req


def get_compose_task_resource_req(token, start=1, count=10,
                                  order='desc', order_by='cpu'):
    # 获取聚合-任务占用资源请求
    req = ApiTemplate()
    req.path = '/gateway/fe-compose/api/v1/task-resource-profiles'
    req.url = urljoin(config.base_url, req.path)
    req.method = 'get'
    req.headers = {'Authorization': token}
    req.param.update({
        "start": start,
        "count": count,
        "order": order,
        "orderBy": order_by,
        "all": "false"
        }
    )
    return req
