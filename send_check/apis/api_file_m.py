# -*- coding: utf-8 -*-

from urllib.parse import urljoin

from configurations import config
from send_check.apis.api_template import ApiTemplate
from utilities.common_method import get_uuid_from_token


def get_upload_file_req(token, file, target):
    # 获取用户uuid
    uuid = get_uuid_from_token(token)
    # 构造上传文件请求
    path = 'file-manager/api/v1/files/upload'
    req = ApiTemplate()
    req.url = urljoin(config.base_url, path)
    req.method = 'post'
    req.headers = {
        "Authorization": token,
        # "Content-Type": "multipart/form-data"
    }
    req.body = {
        "ownerId": uuid,
        "path": target
    }
    # 将文件转化为二进制格式，通过files参数post上传
    req.files = {
        "files": open(r'{}'.format(file), "rb")
    }
    return req


def get_download_file_req(token, filename, target):
    # 获取用户uuid
    uuid = get_uuid_from_token(token)
    # 构造下载文件请求
    path = 'file-manager/api/v1/files/download'
    req = ApiTemplate()
    req.url = urljoin(config.base_url, path)
    req.method = 'get'
    req.param = {
        "ownerId": uuid,
        "path": '{}{}'.format(target, filename)
    }
    req.headers = {
        "Authorization": token
        # "Content-Type": "application/json"
    }
    return req


def get_delete_files_and_folder_req(token, paths):
    # 获取用户uuid
    uuid = get_uuid_from_token(token)
    # 构造删除文件和文件夹名称列表请求
    path = 'file-manager/api/v1/files/delete'
    req = ApiTemplate()
    req.url = urljoin(config.base_url, path)
    req.method = 'post'
    req.headers = {
        "Authorization": token
        # "Content-Type": "application/json"
    }
    req.body = {
        "ownerId": uuid,
        "paths": paths
    }
    return req


def get_create_folder_req(token, target, folder):
    # 获取用户uuid
    uuid = get_uuid_from_token(token)
    # 构造创建文件夹请求
    path = 'file-manager/api/v1/files'
    req = ApiTemplate()
    req.url = urljoin(config.base_url, path)
    req.method = 'post'
    req.headers = {
        "Authorization": token
        # "Content-Type": "application/json"
    }
    req.body = {
        "ownerId": uuid,
        "path": '{}/{}'.format(target, folder)
    }
    return req


def get_copy_file_req(token, sourcePaths, targetPath):
    # 获取用户uuid
    uuid = get_uuid_from_token(token)
    # 构造拷贝文件/文件夹请求
    path = 'file-manager/api/v1/files/copy'
    req = ApiTemplate()
    req.url = urljoin(config.base_url, path)
    req.method = 'post'
    req.headers = {
        "Authorization": token
    }
    req.body = {
        "ownerId": uuid,
        "sourcePaths": sourcePaths,
        "targetPath": targetPath
    }
    return req


def get_move_file_req(token, sourcePaths, targetPath):
    # 获取用户uuid
    uuid = get_uuid_from_token(token)
    # 构造移动文件/文件夹请求
    path = 'file-manager/api/v1/files/move'
    req = ApiTemplate()
    req.url = urljoin(config.base_url, path)
    req.method = 'post'
    req.headers = {
        "Authorization": token
    }
    req.body = {
        "ownerId": uuid,
        "sourcePaths": sourcePaths,
        "targetPath": targetPath
    }
    return req


def get_share_file_req(token, owner_uuid, sharePath, isGlobal=False, users=None, groups=None):
    # 获取用户uuid
    share_uuid = get_uuid_from_token(token)
    # 构造共享文件/文件夹请求
    path = 'file-manager/api/v1/file_shares'
    req = ApiTemplate()
    req.url = urljoin(config.base_url, path)
    req.method = 'post'
    req.headers = {
        "Authorization": token
    }
    req.body = {
        "ownerId": owner_uuid,
        "sharerId": share_uuid,
        "path": sharePath,
        "isGlobal": isGlobal,
        "users": [] if users is None else users,
        "groups": [] if groups is None else groups
    }
    return req


def get_cancel_shared_file_req(token, share_uuid):
    req = ApiTemplate()
    req.path = '/file-manager/api/v1/file_shares'
    req.url = urljoin(config.base_url, req.path)
    req.method = 'delete'
    req.headers = {
        "Authorization": token
    }
    if type(share_uuid) is not list:
        req.param = {
            "uuids": share_uuid
        }
    else:
        req.param = {
            "uuids": share_uuid[0],
            "uuids": share_uuid[1]
        }
    return req


def get_extract_file_req(token, file_path, target_path):
    # 获取用户uuid
    uuid = get_uuid_from_token(token)
    # 构造解压文件请求
    path = 'file-manager/api/v1/files/extract'
    req = ApiTemplate()
    req.url = urljoin(config.base_url, path)
    req.method = 'post'
    req.headers = {
        "Authorization": token,
    }
    req.body = {
        "ownerId": uuid,
        "path": file_path,
        "targetPath": target_path

    }
    return req


def get_rename_file_folder_req(token, sourcepath, newname):
    # 获取用户uuid
    uuid = get_uuid_from_token(token)
    # 构造重命名文件或文件夹请求
    path = 'file-manager/api/v1/files/rename'
    req = ApiTemplate()
    req.url = urljoin(config.base_url, path)
    req.method = 'post'
    req.headers = {
        "Authorization": token,
    }
    req.body = {
        "ownerId": uuid,
        "path": sourcepath,
        "newName": newname
    }
    return req
