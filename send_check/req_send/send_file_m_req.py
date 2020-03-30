# -*- coding: utf-8 -*-
from ast import literal_eval
from send_check.apis import api_file_m, api_compose
from send_check.req_send import send_req
from utilities.common_method import get_uuid_from_token
from utilities.db_operation import query_from_mongodb


def upload_file(token, file, target):
    '''
    上传文件
    :param token:
    :param file: 上传文件及其绝对路径
    :param target: 上传到ceph的目的地址（相对路径）
    :return:
    '''
    req = api_file_m.get_upload_file_req(token=token, file=file, target=target)
    res = send_req.send_request(req)
    return res['files']


def download_file(token, filename, target):
    '''
    下载文件
    :param token:
    :param filename: 下载文件名称
    :param target: 下载文件的ceph地址（相对路径）
    :return: 下载文件内容
    '''
    req = api_file_m.get_download_file_req(token=token, filename=filename, target=target)
    res = send_req.send_request(req)
    return res


def delete_files_and_folders(token, paths):
    '''
    删除文件/文件夹操作
    :param token:
    :param paths: 删除文件和文件夹名称列表
    :param target: 删除文件的ceph地址（相对路径）
    :return:
    '''
    req = api_file_m.get_delete_files_and_folder_req(token=token, paths=paths)
    res = send_req.send_request(req, '204')
    return res


def create_folder(token, target, folder, resultcode='201'):
    '''
    创建文件夹
    :param token:
    :param target: 文件夹路径
    :param folder: 文件夹名称
    :return:
    '''
    req = api_file_m.get_create_folder_req(token=token, target=target, folder=folder)
    res = send_req.send_request(req, resultcode)
    return res


def copy_file(token, sourcePaths, targetPath):
    '''
    拷贝文件/文件夹
    :param token:
    :param sourcePaths:
    :param targetPath:
    :return:
    '''
    req = api_file_m.get_copy_file_req(token=token, sourcePaths=sourcePaths, targetPath=targetPath)
    res = send_req.send_request(req, '202')
    return res


def move_file(token, sourcePaths, targetPath):
    '''
    移动文件/文件夹
    :param token:
    :param sourcePaths:
    :param targetPath:
    :return:
    '''
    req = api_file_m.get_move_file_req(token=token, sourcePaths=sourcePaths, targetPath=targetPath)
    res = send_req.send_request(req)
    return res


def get_file_list(token, path):
    '''
    根据path查询路径下存在的文件/文件夹，并返回文件/文件夹名称列表
    :param token:
    :param ownerid:
    :param path:
    :return:
    '''
    ownerid = get_uuid_from_token(token)
    req = api_compose.get_compose_file_list_req(token=token, owner_id=ownerid, file_path=path)
    res = send_req.send_request(req)
    filename = []
    elements = res['children']
    for i in range(len(elements)):
        filename.append(elements[i]['name'])
    return filename


def extract_file(token, file_path, target_path, resultcode='202'):
    '''
    解压文件
    :param token:
    :param file_path: 压缩文件在ceph的全路径
    :param target_path: 解压到ceph的目的地址（相对路径）
    :return:
    '''
    req = api_file_m.get_extract_file_req(token=token, file_path=file_path, target_path=target_path)
    res = send_req.send_request(req, resultcode)
    return res


def rename_file_folder(token, path, newname, resultcode='200'):
    '''
    重命名文件或文件夹
    :param token:
    :param path: 被重名文件或文件夹全路径
    :param newname: 重命名的名字
    :return:
    '''
    req = api_file_m.get_rename_file_folder_req(token=token, sourcepath=path, newname=newname)
    res = send_req.send_request(req, resultcode)
    return res


def share_file(token, owner_uuid, sharePath, isGlobal=False, users=None, groups=None):
    '''
    分享文件
    :param token:
    :param owner_uuid: 文件拥有者UUID
    :param sharePath: 分享文件的路径
    :param isGlobal:
    :param users:
    :param groups:
    :return:
    '''
    req = api_file_m.get_share_file_req(token=token, owner_uuid=owner_uuid, sharePath=sharePath, isGlobal=isGlobal,
                                        users=users, groups=groups)
    res = send_req.send_request(req, '201')
    return res['uuid']


def share_files_batch(token, sharePaths, owner_id, share_id, isGlobal=False, users=None, groups=None):
    '''
    批量分享文件
    :param token:
    :param owner_uuid: 文件拥有者UUID
    :param sharePaths: 分享文件的路径
    :param isGlobal:
    :param users:
    :param groups:
    :return:
    '''
    req = api_compose.get_compose_file_share_batch_req(token=token, paths=sharePaths, owner_id=owner_id,
                                                       share_id=share_id, is_global=isGlobal, users=users,
                                                       groups=groups)
    res = send_req.send_request(req)
    res_list = literal_eval(res)
    share_uuid = []
    for i in range(len(res_list)):
        share_uuid.append(res_list[i]['uuid'])
    return share_uuid


def cancel_shared_file(token, share_uuid):
    '''
    取消分享文件
    :param token:
    :param share_uuid: 文件分享关系的UUID
    :return:
    '''
    req = api_file_m.get_cancel_shared_file_req(token=token, share_uuid=share_uuid)
    res = send_req.send_request(req, '204')
    return res


def get_shared_file_list(token, owner_id=None, user_id=None):
    '''
    可根据owner_id获取“我的共享”文件信息，也可根据user_id获取“接受的共享”文件信息
    :param token:
    :param owner_id:
    :param user_id:
    :return:
    '''
    req = api_compose.get_compose_shared_file_list_req(token=token, owner_id=owner_id, user_id=user_id)
    res = send_req.send_request(req)
    filename = []
    elements = res['children']
    for i in range(len(elements)):
        filename.append(elements[i]['name'])
    return filename


def get_volume_id_by_user_uuid(user_uuid):
    '''
    通过uuid从monogBD中查询到用户对于的volumn id信息
    :param uuid：
    :return:
    '''
    volume_id = query_from_mongodb(db_name='storage-manager', collection_name='volumes',
                                   query_conditions={'owner_id': user_uuid}, columns={'_id': 1})
    if len(volume_id) != 0:
        return volume_id[0]['_id']
    else:
        return False
